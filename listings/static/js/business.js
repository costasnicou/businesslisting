const showMore = document.querySelector('.overview-read-more');
const overview = document.querySelector('.business-overview');
const overlay = document.querySelector('.overlay');
const galImg = document.querySelectorAll('.gal-img');
const closeImg = document.querySelector('.close-img');

showMore.addEventListener('click',function(e){
    e.preventDefault();
    overview.style.overflow = "initial";
    overview.style.height = "100%";
    showMore.style.display = "none";
});

galImg.forEach(img=>{
    img.addEventListener('click',function(){
      
        overlay.classList.remove('hidden');
        img.classList.add('zoomed');
        closeImg.classList.remove('hidden');


    });

});


closeImg.onclick = function(){
   
    galImg.forEach(img=>{
        img.classList.remove('zoomed');
    })
    
   
    overlay.classList.add('hidden');
    closeImg.classList.add('hidden');

}


