async function generateTrip() {

    const fromLocation =
        document.getElementById("fromLocation").value.trim();

    const destination =
        document.getElementById("destination").value.trim();

    const days =
        document.getElementById("days").value;

    const people =
        document.getElementById("people").value;


    const button =
        document.getElementById("generateBtn");

    const loading =
        document.getElementById("loading");

    const result =
        document.getElementById("result");

    const answer =
        document.getElementById("answer");

    const errorBox =
        document.getElementById("errorBox");


    // Clear old result
    result.classList.add("hidden");

    errorBox.classList.add("hidden");

    answer.innerHTML = "";


    // Validation

    if (!fromLocation) {

        showError(
            "Please enter your starting location."
        );

        return;
    }


    if (!destination) {

        showError(
            "Please enter your destination."
        );

        return;
    }


    if (!days) {

        showError(
            "Please select the number of days."
        );

        return;
    }


    if (!people) {

        showError(
            "Please select the number of people."
        );

        return;
    }



    // Show loading

    loading.classList.remove("hidden");

    button.disabled = true;

    button.innerText =
        "⏳ Generating Travel Plan...";


    try {


        const response = await fetch(
            "/generate",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    from_location:
                        fromLocation,

                    destination:
                        destination,

                    days:
                        days,

                    people:
                        people

                })

            }
        );



        const data =
            await response.json();



        if (!response.ok ||
            !data.success) {

            throw new Error(
                data.error ||
                "Unable to generate travel plan."
            );

        }



        // Display AI answer

        answer.innerHTML =
            formatAIResponse(data.answer);


        result.classList.remove("hidden");


        // Scroll to answer

        result.scrollIntoView({
            behavior: "smooth"
        });


    }


    catch (error) {

        console.error(error);

        showError(
            error.message ||
            "Something went wrong."
        );

    }


    finally {

        loading.classList.add("hidden");

        button.disabled = false;

        button.innerText =
            "✨ Generate AI Travel Plan";

    }

}



function formatAIResponse(text) {

    if (!text) {

        return `
            <p>
                No answer received from Gemini.
            </p>
        `;

    }


    let formatted =
        text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");


    // Bold

    formatted =
        formatted.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    // Headings

    formatted =
        formatted.replace(
            /^### (.*)$/gm,
            "<h3>$1</h3>"
        );


    formatted =
        formatted.replace(
            /^## (.*)$/gm,
            "<h3>$1</h3>"
        );


    formatted =
        formatted.replace(
            /^# (.*)$/gm,
            "<h2>$1</h2>"
        );


    // Bullet points

    formatted =
        formatted.replace(
            /^[\-\*] (.*)$/gm,
            "<li>$1</li>"
        );


    // Numbered points

    formatted =
        formatted.replace(
            /^\d+\.\s+(.*)$/gm,
            "<li>$1</li>"
        );


    // Line breaks

    formatted =
        formatted.replace(
            /\n/g,
            "<br>"
        );


    return formatted;

}



function showError(message) {

    const errorBox =
        document.getElementById("errorBox");


    errorBox.innerText =
        "⚠️ " + message;


    errorBox.classList.remove(
        "hidden"
    );


    errorBox.scrollIntoView({
        behavior: "smooth"
    });

}