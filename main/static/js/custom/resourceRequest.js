//GET AND POST METHOD FOR THE RESOURCES
//get elements. the query selectorAll returns a node-list
{
const elements = {
    //resource_name: document.getElementsByClassName('resource-name'),
    //resource_name: document.querySelectorAll('.resource-name'),
    //resource: document.querySelectorAll('.resource'),
    resource_link: document.querySelectorAll('.resource-link'),
    resource_download: document.querySelectorAll('.resource-download'),
    email_div: document.getElementById('emailResource'),
    email_address: document.getElementById('emailAddress'),
    email_submit: document.querySelectorAll('.email-submit'),
};
    
//convert from nodelist to array
const resource_link_array = Array.from(elements.resource_link);
const email_submit_array = Array.from(elements.email_submit);
//let resource_array = Array.from(elements.resource);
//const resource_download_array = Array.from(elements.resource_download);
//const resource_name_array = Array.from(elements.resource_name);

//assign event listeners to btns
resource_link_array.forEach(el_link => {
    el_link.addEventListener('click', getLink);
});

email_submit_array.forEach(el_btn => {
    el_btn.addEventListener('click', postMail);
});

function getLink(el) {
    //display the email request link
    elements.email_div.classList.toggle("hidden");
    //console.log(filename);
    
};

// when the user interacts with the email box
function postMail(e) {
    // declare a variable object to hold the post data
    let file_content_request;

    // get email address from input
    let email_address = elements.email_address.value;

    // create a post object
    file_content_request = {
        "filename": e.target.id,
        "email": email_address,
    };
    // console.log(file_content_request);

    // hide the email address box
    elements.email_div.classList.add("hidden");
};

/*
let postMail = function() {
    //post request to required path
    fetch(`${window.location.origin}/resources-request`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
}
*/
/*
resource_download_array.forEach(el_dwn => {
    el_dwn.addEventListener('click', download);
});


function download(el) {
    //get resource id from parent div
    parentId = el.target.parentNode.parentNode.id;
    //get the filename
    //let filename = 'link.txt';
    fetch(`${window.location.origin}/download/link.txt`)
        .then(resp => {
        console.log(window.location.origin);
    })
}
*/
}










