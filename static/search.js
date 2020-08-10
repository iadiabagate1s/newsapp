

// $('#formsearchnav').on('submit', function(e){
//    let value = $('#input-bar-btn').val()
//    newshandle2('headlines/search', value)
//     $('input-bar-btn').val('') 



// })


$('#btnbtn').on('click', function(e){

    e.preventDefault()
    let value = $('#searchbar').val()
    $("#cardstrsearch").empty()
   
   

newshandle2('headlines/search', value)
$('#searchbar').val('') 
    
})

async function newshandle2(headlines, word){
    let newsresp = await axios.post(`/${headlines}`, {
        word : word
    })
    
    newsarray = newsresp.data.articles.splice(1, 16)
  

    newsarray.forEach(story => {
      let containercard = $(`<div id='storycard' class="card mx-1 my-1" style="width: 15rem border-0"></div>`)
      let imgcard ;
      
      if (story.urlToImage){
       imgcard = $(`<img src=${story.urlToImage} class="card-img-top" alt="...">`)
 
      }else{
       imgcard= $(`<img src='static/img/no image.png' class="card-img-top" alt="...">`)
      }
      let cardboddiv = $(`<div id='cardbod' class="card-body"></div>`)
      let cardt = $(`<h5 class="card-title">${story.title}</h5>`)
      let cardp = $(`<p class="card-text">${story.description}</p>`)
      let carda = $(`<a href=${story.url} class="btn btn-primary">Full story</a>`)
      let carbtn = $(`<button class='savebtn btn btn-danger' id='bookmark'> Save</button>`)
     
      



      if ($('#welcome').data() ){
        
        cardbody = cardboddiv.append(cardt,cardp, carda, carbtn )
        card = containercard.append(imgcard, cardbody)
        $('#cardstrsearch').append(card)
      }
      else {
        cardbody = cardboddiv.append(cardt,cardp, carda )
        card = containercard.append(imgcard, cardbody)
        return $('#cardstrsearch').append(card)

      }
      


    })
}
