// function to submit a testimonial
function submitTestimonial() {

    let errorMessageContainer = document.getElementById('errorMessage');
    let errorMessage = '';
    errorMessageContainer.innerHTML = errorMessage;


    let nameInput = document.getElementById('name');
    let feedbackInput = document.getElementById('feedback');


    if (nameInput === undefined || nameInput == null || nameInput.value === '' || nameInput.value.length < 5) {
        errorMessage = 'Please enter a valid name. It should be at least 5 characters long.';
    } else if (feedbackInput === undefined || feedbackInput == null || feedbackInput.value === '' || feedbackInput.value.length > 300) {
        errorMessage = 'Please enter a valid feedback. It should be at max 300 characters long.';
    }

    errorMessageContainer.innerHTML = errorMessage;

    if (errorMessage.length === 0) {
        fetch("/testimonial/add/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                name: nameInput.value,
                feedback: feedbackInput.value
            })
        })
            .then(response => {
                if (response.ok) {
                    document.getElementById("testimonialForm").reset();
                    alert("Testimonial submitted successfully!");
                    loadTestimonials();
                } else {
                   alert("Failed to submit testimonial. Please try again.");
                }
            })
            .catch(() => {
                alert("Failed to submit testimonial. Something went wrong.");
            });
    }
}

// function to retrieve all the testimonial
function loadTestimonials() {
    fetch("/testimonial/all/")
        .then(response => {
            if (!response.ok) throw new Error("Failed to fetch testimonials");
            return response.json();
        })
        .then(testimonials => {
            const list = document.getElementById("testimonialList");
            list.innerHTML = "";

            testimonials.forEach(t => {
                const divElement = document.createElement("div");
                divElement.className = "testimonial-item";
                divElement.innerHTML = `<p>"${t.feedback}"</p><p>- ${t.name}</p>`;
                list.appendChild(divElement);
            });
        })
        .catch(err => {
            console.error("Error loading testimonials:", err);
        });
}

// calling load testimonial on app startup
loadTestimonials();
