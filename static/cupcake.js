BASE_URL = 'http://127.0.0.1:5000/api/cupcakes'

const cupcakeList = document.querySelector('#cupcake-list')
const formdata = document.querySelector('.form-data')


function getHtmlForCupcake(cupcake) {
    const div = document.createElement('div');
    div.setAttribute('data-cupcake-id', cupcake.id);
    const li = document.createElement('li');
    li.textContent = `${cupcake.flavor}/${cupcake.rating}/${cupcake.size}`
    const button = document.createElement('button');
    button.classList.add('delete-button');
    button.innerText = 'X';
    li.append(button)
    div.appendChild(li)
    const image = document.createElement('img');
    image.classList.add('cup-image')
    image.setAttribute('src', cupcake.image);
    div.append(image)

    return div;

}
async function getAllCupcakes() {
    const response = await axios.get(BASE_URL)

    for (let cupcake of response.data.cupcakes) {
        let newCupcake = getHtmlForCupcake(cupcake)
        cupcakeList.append(newCupcake)
    }
}

formdata.addEventListener('submit', async function (e) {
    e.preventDefault();
    let flavor = document.getElementById('cup-flavor').value;
    // console.log(`Flavor${flavor}`)
    let size = document.getElementById('cup-size').value;
    let rating = document.getElementById('cup-rating').value;
    let image = document.getElementById('cup-image').value;

    const newCupcakeResponse = await axios.post(BASE_URL, {
        flavor,
        size,
        rating,
        image
    });

    const newCupcake = getHtmlForCupcake(newCupcakeResponse.data.cupcake);
    cupcakeList.append(newCupcake);
    formdata.reset();

    const deleteBtn = document.querySelector('.delete-button');

    deleteBtn.addEventListener('click', async function (e) {
        e.preventDefault();
        let cupcake = e.target.closest('div');
        let cupcake_id = cupcake.dataset.cupcakeId
        await axios.delete(`${BASE_URL}/${cupcake_id}`);
        cupcake.remove();
    })
})
)

getAllCupcakes;