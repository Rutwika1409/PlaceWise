const slides = [

{
title:"Top Placement Influencing Features",
image:"assets/top_features.png",
description:"Most important factors affecting placement outcomes."
},

{
title:"Placement Distribution",
image:"assets/placement_distribution.png",
description:"Distribution of placed and non-placed students."
},

{
title:"Placement Rate by Branch",
image:"assets/branch_placement_rate.png",
description:"Placement performance across different branches."
},

{
title:"CGPA vs Placement",
image:"assets/cgpa_vs_placement.png",
description:"Relationship between CGPA and placement status."
},

{
title:"Internship Impact",
image:"assets/internship_impact.png",
description:"Impact of internships on placement success."
},

{
title:"Coding Skill Impact",
image:"assets/coding_skill_impact.png",
description:"Influence of coding ability on placement probability."
},

{
title:"Communication Skill Impact",
image:"assets/communication_skill_impact.png",
description:"Role of communication skills in placement outcomes."
},

{
title:"Salary Distribution",
image:"assets/salary_distribution.png",
description:"Distribution of salary packages among placed students."
},

{
title:"Correlation Heatmap",
image:"assets/correlation_heatmap.png",
description:"Correlation between dataset features."
}

];

let currentSlide = 0;

function updateSlide() {

    document.getElementById("analyticsImage").src =
        slides[currentSlide].image;

    document.getElementById("imageTitle").innerText =
        slides[currentSlide].title;

    document.getElementById("imageDescription").innerText =
        slides[currentSlide].description;

    document.getElementById("slideCounter").innerText =
        `${currentSlide + 1} / ${slides.length}`;
}

function nextSlide() {

    currentSlide++;

    if (currentSlide >= slides.length) {
        currentSlide = 0;
    }

    updateSlide();
}

function prevSlide() {

    currentSlide--;

    if (currentSlide < 0) {
        currentSlide = slides.length - 1;
    }

    updateSlide();
}

document.addEventListener("keydown", function(event){

    if(event.key === "ArrowRight"){
        nextSlide();
    }

    if(event.key === "ArrowLeft"){
        prevSlide();
    }

});