document.addEventListener("DOMContentLoaded", async function () {
  setupShareButton();
  setupTopNavBar();
  const jobListContainer = document.querySelector(".job-list");
  const currentJobPath = window.location.pathname;
  const category = currentJobPath.split("/")[2].toLowerCase();
  const jobId = currentJobPath.split("/")[3];
  console.log(jobId);
  console.log(category);

async function loadJobsData() {
  try {
    const response = await fetch("/data/jobs.json");
    const data = await response.json();
    return data;
  } catch (err) {
    console.error("Failed to fetch jobs data", err);
    return [];
  }
}

(async function () {
  const data = await loadJobsData();

  if (!data || !Array.isArray(data) || data.length === 0) {
    similarJobsSection.style.display = "none";
    return;
  }

  // Filter same category and exclude current job from main filtering
  const filteredJobs = data
    .filter(job => job.category === category)
    .sort((a, b) => parseInt(b.timestamp) - parseInt(a.timestamp)); // newest to oldest

  const currentJobIndex = filteredJobs.findIndex(job => job.jobid === jobId);

  if (currentJobIndex === -1) {
    console.error("Current job not found.");
    return;
  }

  const currentJob = filteredJobs[currentJobIndex];

  // Get jobs before and after the current job
  const jobsBefore = filteredJobs.slice(currentJobIndex + 1); // Older
  const jobsAfter = filteredJobs.slice(0, currentJobIndex);   // Newer

  // Get the most recent job, ensuring it’s not the current job
  const mostRecentJob = filteredJobs.find(job => job.jobid !== jobId);

  // Collect jobs with priority: 1 most recent + 2 before + 1 after
  const jobsToDisplay = [];

  if (mostRecentJob) jobsToDisplay.push(mostRecentJob);

  // Add two jobs before
  for (let i = 0; i < jobsBefore.length && jobsToDisplay.length < 3; i++) {
    if (jobsBefore[i].jobid !== jobId) {
      jobsToDisplay.push(jobsBefore[i]);
    }
  }

  // Add one job after
  for (let i = 0; i < jobsAfter.length && jobsToDisplay.length < 4; i++) {
    if (jobsAfter[i].jobid !== jobId) {
      jobsToDisplay.push(jobsAfter[i]);
    }
  }

  // Fill from the rest (in case not enough before/after jobs)
  for (let job of filteredJobs) {
    if (jobsToDisplay.length >= 4) break;
    if (job.jobid !== jobId && !jobsToDisplay.some(j => j.jobid === job.jobid)) {
      jobsToDisplay.push(job);
    }
  }


  // Render job cards
  jobsToDisplay.forEach(job => {
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

  console.log(jobsToDisplay);
   // If still empty, hide section
  if (jobsToDisplay.length === 0) {
    document.querySelector(".si-card").style.display = "none";
    return;
  }

})();

  
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

