//GET AND POST METHOD FOR THE RESOURCES
//get elements. the query selectorAll returns a node-list
{
const elements = {
    //resource_name: document.getElementsByClassName('resource-name'),
    resource_name: document.querySelectorAll('.resource-name'),
    resource: document.querySelectorAll('.resource'),
    resource_link: document.querySelectorAll('.resource-link'),
    resource_download: document.querySelectorAll('.resource-download'),
    email_resource: document.getElementById('emailResource'),
};
//convert from nodelist to array
//let resource_array = Array.from(elements.resource);
const resource_link_array = Array.from(elements.resource_link);
const resource_download_array = Array.from(elements.resource_download);
//const resource_name_array = Array.from(elements.resource_name);

//assign event listeners to btns
resource_link_array.forEach(el_link => {
    el_link.addEventListener('click', getLink);
});

resource_download_array.forEach(el_dwn => {
    el_dwn.addEventListener('click', download);
});

function getLink(el) {
    //get resource id from parent div
    parentId = el.target.parentNode.parentNode.id;
    //display the email request link
    elements.email_resource.classList.toggle("hidden");
    //post request to required path
    console.log('get link clicked', parentId)
}

function download(el) {
    //get resource id from parent div
    parentId = el.target.parentNode.parentNode.id;
    console.log('download clicked', parentId)
}



}










