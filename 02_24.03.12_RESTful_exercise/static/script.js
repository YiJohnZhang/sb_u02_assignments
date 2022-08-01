function createNewCupcakeListing(element){

    let newHTMLElementImage = document.createElement('img');
    newHTMLElementImage.setAttribute('src', element['image']);
    newHTMLElementImage.setAttribute('alt', element['flavor']);

    let newHTMLELementDescription = document.createElement('div');
    newHTMLELementDescription.innerText = `Size: ${element['size']}, Rating: ${element['rating']}`

    newHTMLELementDescription.prepend(newHTMLElementImage);

    document
        .getElementById('cupcake_json')
        .appendChild(newHTMLELementDescription);

}

function fetchAllCupcakes(){

    axios.get('/api/cupcakes')
        .then(function(response){

            for (let element of response['data']['cupcakes']){

                createNewCupcakeListing(element);
            }

        })
        .catch(function(error){

            console.log(error);

        });

}

function submitForm(){

    const newCupcakeForm = document.getElementById('newCupcake-form');
    
    const formData = new FormData(newCupcakeForm);
        // https://developer.mozilla.org/en-US/docs/Web/API/FormData/FormData
        
    axios.post('/api/cupcakes', formData)
        .then(function(response){

            console.log(response)
            createNewCupcakeListing(response['data']['cupcake']);

        })
        .catch(function(error){
            console.log(error);
        });

}

document.getElementById('newCupcake-form-submit').addEventListener('click', function(evt){
    //print(evt);   // how to print
    evt.preventDefault();
    submitForm();
});

window.addEventListener('load', fetchAllCupcakes);
    //document.addEventListener('load',...) is unreliable: 