const businesses = document.querySelectorAll('.business');
const loadMore = document.querySelector('.load-more');
const businessWraper = document.querySelector('.all-businesses-frwraper');


let counter = businesses.length;
if (businesses.length < 9){
    loadMore.style.display = "none";

    if (businesses.length == 0){
        const html = `<h3 class="no-results">No Results Found</h3>`;
        businessWraper.insertAdjacentHTML("beforeend",html);
        
    }

}
let quantity = 3;
function load() {

    // Set start and end listing numbers, and update counter
    const start = counter;
    const end = start + quantity;
    counter = end;

    const category = document.querySelector('#category-select').value;
    const city = document.querySelector('#city-select').value;

    
    fetch(
        `/all-listings?start=${start}&end=${end}`
    )
    .then(response => response.json())
    .then(data => {
        data.businesses.forEach(add_listing);
    });


};

// Add a new post with given contents to DOM
function add_listing(contents) {

    const html = `
            <div class="business">
                <div class="business--img" style="
                background: linear-gradient(rgba(39, 39, 39, 0.15),rgba(46, 46, 46, 0.15)), url(${contents.img});
                width:300px;
                height: 200px;
                background-size: cover;
                background-position: center;
                opacity: 0.9;
                border-radius: 5px;">

                </div>

                <h3 class="business-title">${contents.title}</h3>
                <p class="business-desc">${contents.desc.split(" ").slice(0, 7).join(" ")} ...</p>
                <div class="business-details">
                    <p class="phone"><i class="fa-solid fa-phone-volume" style="color: rgb(0, 0, 0);"></i>${contents.phone}</p>
                    <p class="city"><i class="fa-solid fa-location-pin" style="color: rgb(0, 0, 0);"></i>${contents.city}</p>
                </div>

                <div class="business_sub-details">
                    <div class="featured_cat">
                        
                        <img src="${contents.cat_photo}" alt="">
                        
                        <p>${contents.category}</p>
                    </div>

                    <div class="business_sub-details-right">
                        <a href=""><i class="fa-solid fa-eye"></i></a>
                        <p class="tooltip">View More</p>
                    </div>
                </div>
            </div>
    
    `;


    // Add business to DOM
    businessWraper.insertAdjacentHTML("beforeend",html);
   
};