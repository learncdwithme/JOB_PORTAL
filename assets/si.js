document.addEventListener("DOMContentLoaded", async function () {
  setupShareButton();
  setupTopNavBar();
  const jobListContainer = document.querySelector(".job-list");
  const currentJobPath = window.location.pathname;
  const category = currentJobPath.split("/")[2].toLowerCase();
  const jobId = currentJobPath.split("/")[3];

  // Utility to load jobs data
  async function loadJobsData() {
    console.log("data");
    // if (window.cachedJobsData) {
    //   return window.cachedJobsData;
    // }

    // If not cached or invalid, fetch fresh
    try {
      const response = await fetch("/data/jobs.json");
      const data = await response.json();
      window.cachedJobsData = data;
      return data;
    } catch (err) {
      console.error("Failed to fetch jobs data", err);
      return [];
    }
  }
  
  // Use data
  const data = await loadJobsData();
  if (!data || !Array.isArray(data) || data.length === 0) {
    similarJobsSection.style.display = "none";
    console.log(data);
    return;
  } 
  const similarJobs = data.filter(
    (job) => job.category === category && job.jobid !== jobId
  );


  const jobsToDisplay = similarJobs
    .sort((a, b) => parseInt(b.timestamp) - parseInt(a.timestamp))
    .slice(0, 4);

  jobsToDisplay.forEach((job) => {
    const jobCard = document.createElement("div");
    jobCard.classList.add("job-card-sm");
    jobCard.innerHTML = `
      <img src="/assets/cp.svg" alt="${job.company} Logo">
      <h1>${job.role}</h1>
      <p>${job.company}</p>
      <a href="/${job.path}">View Job</a>
    `;
    jobListContainer.appendChild(jobCard);
  });

  if (jobsToDisplay.length === 0) {
    document.querySelector(".si-card").style.display = "none";
  }
});



function setupTopNavBar() {
  const backBtn = document.getElementById('backBtn');
  if (!backBtn) return;

  backBtn.addEventListener('click', () => {
    if (window.history.length > 1) {
      window.history.back(); // Go back in history if available
    } else {
      window.location.href = '/'; // Fallback to homepage
    }
  });
}



function setupShareButton() {
  const shareBtn = document.querySelector('.share-btn');
  if (!shareBtn) return;

  shareBtn.addEventListener('click', () => {
    const shareUrl = window.location.origin + window.location.pathname;
    const shareData = {
      title: document.title || 'Check this job',
      text: 'Check out this job opportunity!',
      url: shareUrl
    };

    if (navigator.share) {
      // Native Web Share API (Mobile + some browsers)
      navigator.share(shareData)
        .then(() => console.log('Shared successfully'))
        .catch(err => console.log('Share cancelled or failed', err));
    } else {
      // Fallback: Copy to clipboard
      navigator.clipboard.writeText(shareUrl)
        .then(() => alert('Job link copied to clipboard!'))
        .catch(() => alert('Failed to copy the job link.'));
    }
  });
}

