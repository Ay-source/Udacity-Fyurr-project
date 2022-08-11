var gen_array = []
var parent_gens = document.querySelector("#genres")
const gens = parent_gens.children
for (let i = 0; i < gens.length; i++) {
  let gen_ = gens[i]
  let attributes = gen_.getAttributeNames()
  if ('selected' == attributes[0])
  {
    gen_array.push(gen_.value)
  }
}

for (let i = 0; i < gens.length; i++){
  let gen = gens[i]
  gen.onclick = function(e) {
    if (e.ctrlKey) {
      var index = gen_array.indexOf(gen.value)
      if (index !== -1)
        gen_array.splice(index, 1)
      else
        gen_array.push(gen.value)
    }
    else
    {
      console.log(gen)
      gen_array = []
      gen_array.push(gen.value)
    }
    console.log("gens", gen_array)
  }
}

var form = document.querySelector('form')
form.onsubmit = function(e) {
  var option = document.createElement('option');
  option.style.display = "none";
  option.text = gen_array;
  parent_gens.appendChild(option)
  parent_gens.value = option.value;
}