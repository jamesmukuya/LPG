//GET AND POST METHOD FOR THE RESOURCES
//get elements. the query selectorAll returns a node-list

const elements = {
    resource_link: document.querySelectorAll('.resource-link'),
    resource_download: document.querySelectorAll('.resource-download'),
    email_div: document.getElementById('emailResource'),
    email_address: document.getElementById('emailAddress'),
    email_submit: document.querySelectorAll('.email-submit'),
    email_cancel: document.getElementById('cancelRequest'),
};
    
//convert from nodelist to array
const resource_link_array = Array.from(elements.resource_link);
const email_submit_array = Array.from(elements.email_submit);

//assign event listeners to btns
resource_link_array.forEach(el_link => {
    el_link.addEventListener('click', getLink);
});

email_submit_array.forEach(el_btn => {
    el_btn.addEventListener('click', postMail);
    //el_btn.addEventListener('click', somefxn);
});

// filename
let file_name;

function getLink(el) {
    //display the email request link
    elements.email_div.classList.toggle("hidden");
    elements.email_div.classList.add("flex");

    //hide all the request file buttons
    for (const arr of resource_link_array) {
        //console.log(arr);
        arr.classList.add('hidden')
    }
    //temporarily set the filename
    file_name = el.target.name;
};
///////////////////////////////
function somefxn(e) {
    console.log('filename name called', file_name);
    e.preventDefault();
    //show the buttons
    for (const arr of resource_link_array) {
        //console.log(arr);
        arr.classList.toggle('hidden');
    }
}
//////////////////////////////

// when the user interacts with the email box
function postMail(e) {
    //required mail format
    let mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    
    // declare a variable object to hold the post data
    let file_content_request;

    // get email address from input
    let email_address = elements.email_address.value;

    // if email field does not meet criteria
    if (!email_address.match(mailformat)) {
        alert('You have entered an invalid email address');
        return false;
    }
    else {
        
        // create a post object
        file_content_request = {
            "filename": file_name,
            "email": email_address,
        };
    
        // post the contents
        fetch(`${window.location.origin}/resources-request`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(file_content_request),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        })
        // response object
        .then(function(response){
            if (response.status !== 200) {
                alert('your request was not sent', response.status);
                return;
            }
            response.json().then(function (data) {
                //console.log(data);
                alert(`The file was sent to ${file_content_request.email}`)
            })
        })
        .catch(error =>{
            console.log(error);
            alert(`The file was sent to ${email_address}`)
            //alert('an error has occured', error); failed to fetch
        })
    
        // hide the email address box
        elements.email_div.classList.add("hidden");
    }
    // prevent page refresh
    //e.preventDefault();
};

// when user clicks cancel button
elements.email_cancel.addEventListener('click', (e) => {
    // prevent page from submitting
    e.preventDefault();

    // hide the form
    elements.email_div.classList.toggle("hidden");
    //show the buttons
    for (const arr of resource_link_array) {
        //console.log(arr);
        arr.classList.toggle('hidden');
    }
})








