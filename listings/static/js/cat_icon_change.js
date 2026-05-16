const categoriesBox = document.querySelectorAll('.featured_category');
categoriesBox.forEach(categoryBox=>{
    categoryBox.addEventListener('mouseenter',function(){
        const initImg = categoryBox.querySelector('img');
        const initImgSrc = initImg.getAttribute('src');
        const initImgName = initImgSrc.split('/').pop().split('.')[0];
        const color = "white";
        initImg.src = `static/imgs/catimgs/${initImgName}-${color}.png`        
    });

    categoryBox.addEventListener('mouseleave',function(){
        const changedImg = categoryBox.querySelector('img');
        const changedImgSrc = changedImg.getAttribute('src');
        const changeImgName = changedImgSrc.split('/').pop().split('.')[0];
        const initImgName = changeImgName.split('-')[0];
        const initImg = changedImg;
        initImg.src = `static/imgs/catimgs/${initImgName}.png`
    });
});


