

const base_url = 'http://localhost:5000'

keybtn = document.querySelector('#keybtn')
keyinut = document.querySelector('#keywordin')

//function to handle adding a keyword to keyword list. appends to DOM and saves to database

keybtn.addEventListener('click',async function(e){
  e.preventDefault()
input = document.querySelector('#keywordin')
let subvalue = input.value

  if (!subvalue){

    console.log('subvalue empty')
    input.value = ('')
    return
  }
  else{
    console.log ('this is value', subvalue)

    resp = await axios.post(`${base_url}/addkeyword`, {
      subject : subvalue,
    })
    console.log(resp)
    $('#wordul'). append(`<li class= 'my-1'>${resp.data[0].keyword} <button class='btn btn-sm btn-warning' id="removeword" data-id=${resp.data[0].keyword_id}type="button"> X </button>  </li>`)
    input.value = ''
  }
})



//function to remove Li from the DOM and remove keyword from database
let $removebutton = $("#removeword")

$('ul').on('click', function(e){
   
    const targetdata = e.target
    const wordid = targetdata.getAttribute('data-id')

    if (targetdata.hasAttribute('data-id')){
        console.log ('we will delete this ', targetdata, wordid)

        deletecup(wordid)
        parentli = targetdata.parentElement
        parentli.remove()
        console.log(`${base_url}/keyword/${wordid}`)
        
    }

    async function deletecup(id){
        res = await axios.delete(`${base_url}/keyword/${id}`)
        console.log (res)
    }




})
