// sendbox.fun — reviews & ratings
// Uses Supabase for auth (magic link) and review storage

const SUPABASE_URL = 'https://vadwseqcxwaucfuryyao.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_2IWtWSi5gvMYWyTYrI3fUw_oMVazwQm';

// Load Supabase JS from CDN
const supabaseScript = document.createElement('script');
supabaseScript.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
supabaseScript.onload = initReviews;
document.head.appendChild(supabaseScript);

let supabase = null;
let currentUser = null;
let currentToolId = null;

async function initReviews() {
  supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  // Detect tool ID from URL (/tools/<id>)
  const match = window.location.pathname.match(/\/tools\/([^\/]+)/);
  if (!match) return;
  currentToolId = match[1].replace(/\.html$/, '');

  // Check for auth session
  const { data: { session } } = await supabase.auth.getSession();
  currentUser = session?.user || null;

  // Listen for auth changes
  supabase.auth.onAuthStateChange((event, session) => {
    currentUser = session?.user || null;
    renderReviewBox();
  });

  renderReviewBox();
  loadReviews();
}

async function loadReviews() {
  if (!currentToolId) return;

  const { data: reviews, error } = await supabase
    .from('reviews')
    .select('rating, review_text, user_email, created_at')
    .eq('tool_id', currentToolId)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Failed to load reviews:', error);
    return;
  }

  // Compute aggregate
  const count = reviews?.length || 0;
  const avg = count > 0 ? (reviews.reduce((s, r) => s + r.rating, 0) / count).toFixed(1) : 0;

  renderRatingSummary(avg, count);
  renderReviews(reviews || []);
}

function renderRatingSummary(avg, count) {
  const el = document.getElementById('rating-summary');
  if (!el) return;
  if (count === 0) {
    el.innerHTML = '<span style="color:var(--text-light);font-size:14px;">No reviews yet — be the first!</span>';
    return;
  }
  const stars = '★'.repeat(Math.round(avg)) + '☆'.repeat(5 - Math.round(avg));
  el.innerHTML = `<span style="color:#F59E0B;font-size:18px;">${stars}</span> <strong>${avg}</strong> <span style="color:var(--text-light);">· ${count} review${count !== 1 ? 's' : ''}</span>`;
}

function renderReviews(reviews) {
  const el = document.getElementById('reviews-list');
  if (!el) return;
  if (reviews.length === 0) {
    el.innerHTML = '';
    return;
  }
  el.innerHTML = reviews.map(r => {
    const stars = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
    const email = (r.user_email || '').replace(/(.{2}).+@.+/, '$1***');
    const date = new Date(r.created_at).toLocaleDateString();
    return `<div class="review-item">
      <div class="review-head">
        <span class="review-stars">${stars}</span>
        <span class="review-meta">${email} · ${date}</span>
      </div>
      ${r.review_text ? `<p class="review-text">${escapeHtml(r.review_text)}</p>` : ''}
    </div>`;
  }).join('');
}

function renderReviewBox() {
  const el = document.getElementById('review-box');
  if (!el) return;

  if (!currentUser) {
    el.innerHTML = `
      <h3>Write a review</h3>
      <p style="color:var(--text-light);font-size:14px;margin-bottom:12px;">Sign in with email to rate this tool. We'll send you a magic link.</p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <input type="email" id="review-email" placeholder="you@email.com" style="flex:1;min-width:200px;padding:10px 14px;border:1px solid var(--border);border-radius:8px;font-size:14px;">
        <button onclick="sendMagicLink()" style="background:var(--accent);color:white;border:none;padding:10px 20px;border-radius:8px;font-weight:600;cursor:pointer;">Send magic link</button>
      </div>
      <p id="auth-status" style="font-size:13px;margin-top:8px;color:var(--text-light);"></p>`;
    return;
  }

  el.innerHTML = `
    <h3>Write a review</h3>
    <p style="color:var(--text-light);font-size:14px;margin-bottom:12px;">Signed in as ${currentUser.email} · <a href="#" onclick="signOut();return false;" style="color:var(--accent);">sign out</a></p>
    <div id="star-picker" style="font-size:32px;color:#D1D5DB;cursor:pointer;margin-bottom:12px;">
      ${[1,2,3,4,5].map(n => `<span data-rating="${n}" onclick="setRating(${n})" onmouseover="hoverRating(${n})" onmouseout="hoverRating(0)" style="padding:0 2px;">★</span>`).join('')}
    </div>
    <textarea id="review-text" placeholder="Share your experience with this tool (optional)" style="width:100%;padding:12px;border:1px solid var(--border);border-radius:8px;font-size:14px;min-height:80px;resize:vertical;font-family:inherit;"></textarea>
    <button onclick="submitReview()" style="background:var(--accent);color:white;border:none;padding:12px 24px;border-radius:8px;font-weight:600;cursor:pointer;margin-top:12px;">Submit review</button>
    <p id="submit-status" style="font-size:13px;margin-top:8px;color:var(--text-light);"></p>`;
}

let selectedRating = 0;

window.setRating = function(n) {
  selectedRating = n;
  document.querySelectorAll('#star-picker span').forEach((el, i) => {
    el.style.color = i < n ? '#F59E0B' : '#D1D5DB';
  });
};

window.hoverRating = function(n) {
  document.querySelectorAll('#star-picker span').forEach((el, i) => {
    if (n === 0) {
      el.style.color = i < selectedRating ? '#F59E0B' : '#D1D5DB';
    } else {
      el.style.color = i < n ? '#FBBF24' : '#D1D5DB';
    }
  });
};

window.sendMagicLink = async function() {
  const email = document.getElementById('review-email').value.trim();
  const status = document.getElementById('auth-status');
  if (!email || !email.includes('@')) {
    status.textContent = 'Enter a valid email.';
    status.style.color = '#DC2626';
    return;
  }
  status.textContent = 'Sending...';
  status.style.color = 'var(--text-light)';
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: { emailRedirectTo: window.location.href }
  });
  if (error) {
    status.textContent = 'Error: ' + error.message;
    status.style.color = '#DC2626';
  } else {
    status.textContent = '✓ Check your email for a magic link.';
    status.style.color = '#10B981';
  }
};

window.signOut = async function() {
  await supabase.auth.signOut();
  currentUser = null;
  renderReviewBox();
};

window.submitReview = async function() {
  const status = document.getElementById('submit-status');
  if (selectedRating < 1) {
    status.textContent = 'Please select a star rating.';
    status.style.color = '#DC2626';
    return;
  }
  const reviewText = document.getElementById('review-text').value.trim();
  status.textContent = 'Submitting...';
  status.style.color = 'var(--text-light)';

  const { error } = await supabase.from('reviews').upsert({
    tool_id: currentToolId,
    user_id: currentUser.id,
    user_email: currentUser.email,
    rating: selectedRating,
    review_text: reviewText || null,
  }, { onConflict: 'tool_id,user_id' });

  if (error) {
    status.textContent = 'Error: ' + error.message;
    status.style.color = '#DC2626';
  } else {
    status.textContent = '✓ Review submitted. Thanks!';
    status.style.color = '#10B981';
    selectedRating = 0;
    document.getElementById('review-text').value = '';
    loadReviews();
  }
};

function escapeHtml(s) {
  const div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}
