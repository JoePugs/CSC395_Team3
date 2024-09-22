let ingredients = [];
let selectedBrand = '';

// button stuff
document.getElementById('add-ingredient').addEventListener('click', function() {
    const ingredientInput = document.getElementById('ingredient');
    const ingredient = ingredientInput.value.trim();

// brand button
document.getElementById('brand-select').addEventListener('change', function() {
    selectedBrand = this.value;

});
    // save ingredients in lsit
    if (ingredient) {
        ingredients.push(ingredient);
        const li = document.createElement('li');
        li.textContent = ingredient;
        document.getElementById('ingredient-list').appendChild(li);
        ingredientInput.value = '';
    }

});