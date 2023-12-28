document.addEventListener("DOMContentLoaded", function () {
    const foodSpot = getFoodSpotDetails();
  
    if (foodSpot) {
      showFoodDetails(foodSpot);
    } else {
      alert("Food spot not found.");
      window.location.href = "./index.html"; // Redirect to the main page
    }
  });
  
  function showFoodDetails(foodSpot) {
    const detailsContainer = document.getElementById("foodDetails");
    detailsContainer.innerHTML = "";
  
    const detailsElement = document.createElement("div");
    detailsElement.classList.add("food-details");
    detailsElement.innerHTML = `
      <!-- Header -->
      <nav class="navbar navbar-dark navbar-expand-sm" style="background-color: #0e1827;">
        <a class="navbar-brand" href="./index.html" style="background-color: #0e1827; display: inline-block; text-align: center;">
          <img src="./img/CamBuzz_logo.png" height="50" class="d-inline-block align-top" alt=""><br />
          CamBuzz
        </a>
      </nav>
  
      <!-- Food Spot Details -->
      <div class="mt-3">
        <h2>${foodSpot.name}</h2>
        <p>${foodSpot.description}</p>
      </div>
  
      <!-- Reviews Section -->
      <div class="review-container">
        <h3>Reviews</h3>
        ${renderReviews(foodSpot.reviews)}
      </div>
  
      <!-- Add Review Section -->
      <div class="add-review-form mt-3">
        <h3>Add a Review</h3>
        <textarea id="newReview" class="form-control" rows="2" placeholder="Write your review..."></textarea>
        <button class="btn btn-primary" onclick="addReview('${foodSpot.name}')">Submit Review</button>
      </div>
    `;
  
    detailsContainer.appendChild(detailsElement);
  }
  
  function renderReviews(reviews) {
    if (reviews && reviews.length > 0) {
      return reviews.map(review => `
        <div class="review">
          <p>${review}</p>
          <button class="btn btn-outline-primary like-button">Like</button>
          <!-- Add ratings or any other details here -->
        </div>
      `).join('');
    } else {
      return '<p>No reviews available.</p>';
    }
  }
  
  function addReview(foodName) {
    const newReview = document.getElementById("newReview").value;
    const foodSpot = getFoodSpotDetails();
  
    if (newReview && foodSpot) {
      foodSpot.reviews.push(newReview);
      showFoodDetails(foodSpot);
    } else {
      alert("Please enter a review.");
    }
  }
  
  function getFoodSpotDetails() {
    const foodSpotName = getFoodSpotNameFromURL();
    const foodSpot = foodSpots.find(foodSpot => foodSpot.name === foodSpotName);
    return foodSpot;
  }
  
  function getFoodSpotNameFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('name');
  }
  