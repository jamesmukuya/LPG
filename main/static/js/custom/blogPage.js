// GET PAGE ELEMENTS

const blogPageElements = {
  comment_btn: document.querySelectorAll('.comment-btn'),
  post_comment: document.querySelectorAll('.post-comment')
}

// add event listeners to the elements
for (c_btn of blogPageElements.comment_btn) {
  c_btn.addEventListener('click', display_hide_textarea);
}

for (p_btn of blogPageElements.post_comment) {
  p_btn.addEventListener('click', postComment);
}

// test //
function btnclick(e) {
  //e.preventDefault()
  console.log('button clicked',e.target.id)
}

// when the comment btn is clicked
function display_hide_textarea(el) {
  // get id of the button that clicked and split to attain base id
  let base_id = el.target.id.split('comm_')[1];
  // get required textarea div using text_+base_id
  let textarea_div = document.getElementById('text_' + base_id);
  // toggle hidden attr of the textarea
  textarea_div.classList.toggle('hidden');
}


function postComment(el) {
  // get base id
  let base_id = parseInt(el.target.id.split('post_')[1]);
  // get text area content
  let contentArea = document.getElementById('comment_reply_' + base_id);
  let content = contentArea.value;

  // if content is empty
  if (content === '') {
    return;
  }
  // create context object  
  ctx = {
    post_id: base_id,
    post_content: content,
  }
  
  // post the contents to blog/reply
  fetch(`${window.location.origin}/blog/reply`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(ctx),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    // response object
    .then(function (response) {
      if (response.status !== 200) {
        alert('your post was not sent', response.status);
        return;
      }
      response.json().then(function (data) {
        console.log('response data',data);
        //alert(`The file was sent to ${file_content_request.email}`)
      })
    })
    .catch(error => {
      console.log(error);
      //alert('an error has occured', error); failed to fetch
    })
  // get required textarea div using text_+base_id
  textarea_div = document.getElementById('text_' + String(base_id));
  // toggle hidden attr of the textarea
  textarea_div.classList.toggle('hidden');
  // prevent page refresh
  // el.preventDefault();
}