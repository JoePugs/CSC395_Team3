let ingredients = [];
let selectedBrand = '';

// Brand button
document.getElementById('brand-select').addEventListener('change', function() {
    selectedBrand = this.value;
    
    // Test
    console.log('Selected Brand:', selectedBrand);
});

// Button stuff
document.getElementById('add-ingredient').addEventListener('click', function() {
    const ingredientInput = document.getElementById('ingredient');
    const ingredient = ingredientInput.value.trim();

    // Save ingredients in list
    if (ingredient) {
        ingredients.push(ingredient);
        const li = document.createElement('li');
        li.textContent = ingredient;
        document.getElementById('ingredient-list').appendChild(li);
        ingredientInput.value = '';
    }
});

function sendPrompt() {
//    const formData = {
//      ingredients: document.getElementById("ingredients").value,
//      brand: document.getElementById("brand").value,
//    };

    const formData = {
      ingredients: "Turkey",
      brand: "Kraft",
    };
  
    fetch('http://localhost:5002/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          document.getElementById("reply_code").value = data.ollama_reply;
          document.getElementById("reply_answer").value = data.reply;
        } else {
          document.getElementById("reply_code").value = data.ollama_reply;
          document.getElementById("reply_answer").value = 'Error';
          alert("Error occurred while processing form: " + data.error);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

document.getElementById('send-json').addEventListener('click', sendPrompt);
