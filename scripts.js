document.getElementById('add-ingredient').addEventListener('click', function() {
    const ingredientInput = document.getElementById('ingredient');
    const ingredient = ingredientInput.value.trim();

    if (ingredient) {
        const li = document.createElement('li');
        li.textContent = ingredient;
        document.getElementById('ingredient-list').appendChild(li);
        ingredientInput.value = '';
    }
});