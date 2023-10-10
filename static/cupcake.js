"use strict";

//not include localhost, make it api/cupcakes
const apiURL = "/api";
const $addCupcakeForm = $('#add-new-cupcake');
const $cupcakeList = $('#all-cupcakes');
const $flavor = $('#flavor');
const $size = $('#size');
const $rating = $('#rating');
const $image = $('#image-url');
const $deleteCupcake = $('#delete');


/**
 * Getting existing cupcakes from API and render to DOM
 */
async function showAllCupcakes() {

  //TODO:make response its own function
  const response = await fetch(`${apiURL}/cupcakes`);
  const cupcakeData = await response.json();
  // console.log(cupcakeData);
  // console.log(cupcakeData.cupcakes[0].flavor);

  for (let cupcake of cupcakeData.cupcakes) {
    let $newCupcake = $(createCupcakeLi(cupcake));
    $cupcakeList.append($newCupcake);
  }

}

/**
 * Generate HTML <li> with a given cupcake
 */
// function createCupcakeLi({id, flavor, size, rating, image_url}) {
// TODO:destructure
function createCupcakeLi(cupcake) {

  const $cupcake = $(`
        <div id="${cupcake.id}">
        <li>
        <p>Flavor:${cupcake.flavor}</p>
        <p>Size:${cupcake.size}</p>
        <p>Rating:${cupcake.rating}</p>
        </li>
        <button id="delete">Delete</button>
        <img src = "${cupcake.image_url}" style="max-width:300px">
       </div>
      `);
  return $cupcake;
}


/**
 * add event listener to ADD button when adding a new cupcake
 */
$addCupcakeForm.on('submit', addNewCupcake);


/**
 * Handle form submission of adding a new cupcake
 */
async function addNewCupcake(evt) {
  evt.preventDefault();

  const newCupcakeData = {
    flavor: $flavor.val(),
    size: $size.val(),
    rating: $rating.val(),
    image_url: $image.val()
  };

  const response = await fetch(`${apiURL}/cupcakes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newCupcakeData),
  });

  //getting response back from post request and render back to html
  const newCupcakeResponse = await response.json();
  let $newCupcake = $(createCupcakeLi(newCupcakeResponse.cupcake));
  $cupcakeList.append($newCupcake);

  $addCupcakeForm.trigger('reset');
  // $flavor.val('');
  // $size.val('');
  // $rating.val('');
  // $image.val('');
}


/**
 * add event listener to DELETE button when adding a new cupcake
 */
$cupcakeList.on('click', '#delete', deleteCupcake);

/**
 * Handle form submission of deleting a cupcake
 */
async function deleteCupcake(evt) {

  const $targetCupcake = $(evt.target).closest('div');
  const targetID = $targetCupcake.attr('id');

  const response = await fetch(`${apiURL}/cupcakes/${targetID}`, {
    method: 'DELETE',
  });
  //do I need a header? NO

  $targetCupcake.remove();

}


showAllCupcakes();
