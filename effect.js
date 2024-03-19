class Accordion {
    constructor(el) {
      // Store the <details> element
      this.el = el;
      // Store the <summary> element
      this.summary = el.querySelector('summary');
      // Store the <div class="content"> element
      this.content = el.querySelector('.content');
  
      // Store the animation object (so we can cancel it if needed)
      this.animation = null;
      // Store if the element is closing
      this.isClosing = false;
      // Store if the element is expanding
      this.isExpanding = false;
      // Detect user clicks on the summary element
      this.summary.addEventListener('click', (e) => this.onClick(e));
    }
  
    onClick(e) {
      // Stop default behaviour from the browser
      e.preventDefault();
      // Add an overflow on the <details> to avoid content overflowing
      this.el.style.overflow = 'hidden';
      // Check if the element is being closed or is already closed
      if (this.isClosing || !this.el.open) {
        this.open();
      // Check if the element is being openned or is already open
      } else if (this.isExpanding || this.el.open) {
        this.shrink();
      }
    }
  
    shrink() {
      // Set the element as "being closed"
      this.isClosing = true;
      
      // Store the current height of the element
      const startHeight = `${this.el.offsetHeight}px`;
      // Calculate the height of the summary
      const endHeight = `${this.summary.offsetHeight}px`;
      
      // If there is already an animation running
      if (this.animation) {
        // Cancel the current animation
        this.animation.cancel();
      }
      
      // Start a WAAPI animation
      this.animation = this.el.animate({
        // Set the keyframes from the startHeight to endHeight
        height: [startHeight, endHeight]
      }, {
        duration: 400,
        easing: 'ease-out'
      });
      
      // When the animation is complete, call onAnimationFinish()
      this.animation.onfinish = () => this.onAnimationFinish(false);
      // If the animation is cancelled, isClosing variable is set to false
      this.animation.oncancel = () => this.isClosing = false;
    }
  
    open() {
      // Apply a fixed height on the element
      this.el.style.height = `${this.el.offsetHeight}px`;
      // Force the [open] attribute on the details element
      this.el.open = true;
      // Wait for the next frame to call the expand function
      window.requestAnimationFrame(() => this.expand());
    }
  
    expand() {
      // Set the element as "being expanding"
      this.isExpanding = true;
      // Get the current fixed height of the element
      const startHeight = `${this.el.offsetHeight}px`;
      // Calculate the open height of the element (summary height + content height)
      const endHeight = `${this.summary.offsetHeight + this.content.offsetHeight}px`;
      
      // If there is already an animation running
      if (this.animation) {
        // Cancel the current animation
        this.animation.cancel();
      }
      
      // Start a WAAPI animation
      this.animation = this.el.animate({
        // Set the keyframes from the startHeight to endHeight
        height: [startHeight, endHeight]
      }, {
        duration: 400,
        easing: 'ease-out'
      });
      // When the animation is complete, call onAnimationFinish()
      this.animation.onfinish = () => this.onAnimationFinish(true);
      // If the animation is cancelled, isExpanding variable is set to false
      this.animation.oncancel = () => this.isExpanding = false;
    }
  
    onAnimationFinish(open) {
      // Set the open attribute based on the parameter
      this.el.open = open;
      // Clear the stored animation
      this.animation = null;
      // Reset isClosing & isExpanding
      this.isClosing = false;
      this.isExpanding = false;
      // Remove the overflow hidden and the fixed height
      this.el.style.height = this.el.style.overflow = '';
    }
  }
  
  document.querySelectorAll('details').forEach((el) => {
    new Accordion(el);
  });


  const convertButton = document.getElementById('convert-button');

  const convertButtonDiv = document.getElementById('convert-button-div');
  const convertInputDiv = document.getElementById('convert-input-div');
  const loader = document.getElementById('loader');
  const downloadingMessage = document.getElementById('downloading-message');
  const errordownloadMessage = document.getElementById('errordownload-message');       
  const downloadMessage = document.getElementById('download-message');        

  const uploadButton = document.getElementById('upload-button');
  const urlInput = document.getElementById('url-input');
  const downloader = document.getElementById('downloader');
  let urlRegex = /docsend\.com\/view\//;
  convertButton.addEventListener('click', function(event) {
          loader.style.display = 'block';  // Show loading icon
      convertButton.style.display = 'none';
      convertButtonDiv.style.display = 'none';
      convertInputDiv.style.display = 'none';

      const url = document.getElementById('url-input').value;
      const data = { url: url };
      document.getElementById('error-message').style.display = 'none';
      const errorMessage = document.getElementById('error-message');
      const normalMessage = document.getElementById('normal-message');

      console.log(data);
      // fetch('http://127.0.0.1:5000/convert', {
      if (urlRegex.test(url)) {
          console.log("success");
          // Your conversion logic goes here when the URL is valid
          loader.style.display = 'block';  // Hide loading icon when done
          // You would also handle showing the downloader or upload button here
//                fetch('https://7124-188-43-253-73.ngrok-free.app/convert', {
         errorMessage.style.display = 'none';
         normalMessage.style.display = 'none';
         urlInput.style.display = 'none';
         downloadingMessage.style.display = 'block';
         fetch('https://c920-18-118-218-235.ngrok-free.app/convert', {
        //  fetch('http://127.0.0.1:5000/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
          })
          .then(response => {
            if (!response.ok) {
              loader.style.display = 'none';  // Hide loading icon
              errordownloadMessage.style.display = 'block';
              downloadingMessage.style.display = 'none';   
              urlInput.style.display = 'none';   
              throw new Error('Network response was not ok');

            }
            return response.json();
          })
          .then(data => {
              console.log('Success:', data);
              loader.style.display = 'none';  // Hide loading icon
              uploadButton.style.display = 'block';  // Show upload button
              downloadMessage.style.display = 'block';
              downloadingMessage.style.display = 'none';   
              urlInput.style.display = 'none';                 
              uploadButton.addEventListener('click', function() {
//                    window.location.href = data.pdf_url;  // Trigger PDF download
              downloader.style.display = 'block'; 
              // data.pdf_id = '65ce3f8794b440ffb908769d';
              fetch('https://c920-18-118-218-235.ngrok-free.app/download/' + data.pdf_id, {
                  // fetch('http://127.0.0.1:5000/download/' + data.pdf_id, {
                          method: 'POST'
                      })
                      .then(response => response.blob())
                      .then(blob => {
                          const url = window.URL.createObjectURL(new Blob([blob]));
                          const a = document.createElement('a');
                          a.href = url;
                          a.download = data.pdf_id+'.pdf';
                          document.body.appendChild(a);
                          a.click();
                          window.URL.revokeObjectURL(url);
                          document.body.removeChild(a);
                          downloader.style.display = 'none';


                      })
                      .catch(error => {
                          console.error('Error:', error);
                          
                          // Hide loading icon in case of error
                          downloader.style.display = 'none';
                      });
              });
          })
          .catch((error) => {
              console.error('Error:', error);
              loader.style.display = 'none';  // Hide loading icon on error
          });                
      } else {
          // Show error message if URL is invalid
          loader.style.display = 'none';
          // errorMessage.textContent = 'Please enter a valid DocSend URL';
          errorMessage.style.display = 'block'; // Show error message
          normalMessage.style.display = 'none';                         
      }                     
  });        
  document.getElementById("url-input").addEventListener("keydown", function(event) {
      if (event.key === "Enter") {
          event.preventDefault();
          loader.style.display = 'block';  // Show loading icon
      convertButton.style.display = 'none';
      convertButtonDiv.style.display = 'none';
      convertInputDiv.style.display = 'none';

      const url = document.getElementById('url-input').value;
      const data = { url: url };
      document.getElementById('error-message').style.display = 'none';
      const errorMessage = document.getElementById('error-message');
      const normalMessage = document.getElementById('normal-message');

      console.log(data);
      // fetch('http://127.0.0.1:5000/convert', {

          
      if (urlRegex.test(url)) {
          console.log("suces");
          // Your conversion logic goes here when the URL is valid
          loader.style.display = 'block';  // Hide loading icon when done
          // You would also handle showing the downloader or upload button here
//                fetch('https://7124-188-43-253-73.ngrok-free.app/convert', {
         errorMessage.style.display = 'none';
         normalMessage.style.display = 'none'; 
         urlInput.style.display = 'none';
         downloadingMessage.style.display = 'block';
         fetch('https://c920-18-118-218-235.ngrok-free.app/convert', {
//                fetch('http://127.0.0.1:5000/convert', {

          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
          })
          .then(response => {
            if (!response.ok) {
              loader.style.display = 'none';  // Hide loading icon
              errordownloadMessage.style.display = 'block';
              downloadingMessage.style.display = 'none';   
              urlInput.style.display = 'none';   
              throw new Error('Network response was not ok');

            }
            return response.json();
          })
          .then(data => {
              console.log('Success:', data);
              loader.style.display = 'none';  // Hide loading icon
              uploadButton.style.display = 'block';  // Show upload button
              downloadMessage.style.display = 'block';
              downloadingMessage.style.display = 'none';   
              urlInput.style.display = 'none';                 
              uploadButton.addEventListener('click', function() {
//                    window.location.href = data.pdf_url;  // Trigger PDF download
              downloader.style.display = 'block'; 
              // data.pdf_id = '65ce3f8794b440ffb908769d';
              fetch('https://c920-18-118-218-235.ngrok-free.app/download/' + data.pdf_id, {
                          method: 'POST'
                      })
                      .then(response => response.blob())
                      .then(blob => {
                          const url = window.URL.createObjectURL(new Blob([blob]));
                          const a = document.createElement('a');
                          a.href = url;
                          a.download = 'converted.pdf';
                          document.body.appendChild(a);
                          a.click();
                          window.URL.revokeObjectURL(url);
                          document.body.removeChild(a);
                          downloader.style.display = 'none';


                      })
                      .catch(error => {
                          console.error('Error:', error);
                          
                          // Hide loading icon in case of error
                          downloader.style.display = 'none';
                      });
              });
          })
          .catch((error) => {
              console.error('Error:', error);
              loader.style.display = 'none';  // Hide loading icon on error
          });                
      } else {
          // Show error message if URL is invalid
          loader.style.display = 'none';
          // errorMessage.textContent = 'Please enter a valid DocSend URL';
          errorMessage.style.display = 'block'; // Show error message
          normalMessage.style.display = 'none';                         
      }            
      }          
  });