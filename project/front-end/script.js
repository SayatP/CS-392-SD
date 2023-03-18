const buy_url = "http://localhost:8000/products/";
const productList = document.querySelector("#products");

async function getItems() {
  const list_url = "http://localhost:8000/products?offset=0&limit=20";
  let response = await fetch(list_url, {
    mode: "cors",
    credentials: "include",
  });

  response = await response.json();
  return response;
}

async function insertProductList(products) {
  productList.innerHTML = "";
  products.forEach((x) => {
    productList.innerHTML += ` <section>
    <figure>
      <img src="${x.image_src}"
      width="500px"
      >
      <figcaption>${x.title}</figcaption>  
      <p>${x.price}$</p>
    </figure>
    <button id=${x.id}>
           Buy
      </button>
  </section>
  `;
  });
  const btns = document.querySelectorAll("button");

  btns.forEach((btn) => {
    btn.addEventListener("click", (event) => {
      const btn = event.currentTarget;
      fetch(buy_url + btn.id + "/buy");
    });
  });
}

getItems().then((products) => insertProductList(products));
