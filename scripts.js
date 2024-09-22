let ingredients = [];
let selectedBrand = '';


// brand button
document.getElementById('brand-select').addEventListener('change', function() {
    selectedBrand = this.value;
    
    // test
    console.log('Selected Brand:', selectedBrand);
});

// button stuff
document.getElementById('add-ingredient').addEventListener('click', function() {
    const ingredientInput = document.getElementById('ingredient');
    const ingredient = ingredientInput.value.trim();

    // save ingredients in lsit
    if (ingredient) {
        ingredients.push(ingredient);
        const li = document.createElement('li');
        li.textContent = ingredient;
        document.getElementById('ingredient-list').appendChild(li);
        ingredientInput.value = '';
    }

});

// make prompt & send to server

function sendPrompt(){
    if (ingredients.length === 0 || !selectedBrand){
        alert('You need to add ingredients and select a brand of products to use');
        return;
    }

    const prompt = "Make me an easy recipe using ${ingredients.join', ')} and items from ${selectedBrand}.";
    const data = {
        prompt: prompt
    };

    // server send
    fetch('http://localhost:5000/json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',

        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        console.log('Success:', result);
    })
    .catch(error => {
        console.error('Error:', error);
    });

}
document.getElementById('send-json').addEventListener('click', sendPrompt);