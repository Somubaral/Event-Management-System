async function loadVenues(){

    const response = await fetch(
        "/api/venues/",
        {
            headers: authHeaders()
        }
    );

    const result =
        await response.json();

    const container =
        document.getElementById(
            "venues-container"
        );

    container.innerHTML = "";

    result.data.forEach(venue => {

        container.innerHTML += `

        <div class="card mb-3">

            <div class="card-body">

                <h5>${venue.name}</h5>

                <p>
                    ${venue.location}
                </p>

                <p>
                    Capacity:
                    ${venue.capacity}
                </p>

            </div>

        </div>

        `;

    });

}

loadVenues();