
openweather_api = '7b70bf3314ed64799900c0b315a53df2'
let status = $('.status')
let loca = $('.location')
let wind = $('.wvalue')
let temperature = $('.tvalue')
let humidity= $('.hvalue')
let icon = $('#icon')

icon.append(`<img id= 'wicon' src=http://openweathermap.org/img/wn/02d.png alt="">`)




// save an article to database function(likes)
async function savearticle( url, title , description){
  resp = await axios.post(`http://localhost:5000/save`,{

  url,
  title, 
  description,
  })
console.log('new like -----', resp)
}

//unsave article from databse (likes) function
async function unsavearticle( title){
  resp = await axios.post(`/save/remove/${title}`,{
  })
console.log('removelike -----', resp)
}

//on button click call either the save function and add class to div containing article info

$('.savebtn').on('click', function (e){
  console.log('clicked saved')
  $(this).parent().toggleClass('bg')

  sibarray =$(this).siblings()
  title =sibarray[0].textContent
  description =sibarray[1].textContent
  url =sibarray[2].getAttribute('href')
            console.log('title----', title)
            console.log('description----', description)
            console.log('url----', url)
            

if ( $(this).text() == 'save'){
   $(this).text('unsave')
   savearticle( title, url, description)
 }else{
  $(this).text('save') 
  unsavearticle(title)
 }
})

//on click of unsave call unsave function and change styling by removing class
$('.removesave').on('click', function(e){

  let title = $(this).siblings()[0].textContent
 unsavearticle(title)
 $(this).parent().parent().remove()

})




//--------------IF USER-----------Logged in ---------------------------------------
if ($('#welcome').data() ){
  console.log('--------user in  session')
  
  placeSearch({
    key: 'eotpicYMnWHOwiNYfxZAfi8vMOizbSdE',
    container: document.querySelector('#place-search-input'),
    useDeviceLocation : true,
  }).on('change', async (e) => {
        $('#wicon').detach()
        $('#barcont').addClass('move')
        $('#cardstr').empty()
        let longitude = e.result.latlng.lng
        let latitude = e.result.latlng.lat
        let place = e.result.value
        let countrycode = e.result.countryCode

        console.log ('lat', latitude)
        console.log ('lon', longitude)
        console.log ('place', place)
        console.log ('country code', countrycode)


// get weather data from server and maker by using location input
       async function getweather(){

        
        let resp = await axios.post('/weather', {
        latitude : latitude,
        longitude : longitude,
        countrycode : countrycode

        
    })
    addData(place, resp)
    }
    getweather()
    newshandle('headlines', countrycode)

    })
    


//-------------------IF USER-----------not logged in ------------------------------

}else {

  console.log('no user logged in')
  
 

placeSearch({
    key: 'eotpicYMnWHOwiNYfxZAfi8vMOizbSdE',
    container: document.querySelector('#place-search-input'),
    useDeviceLocation : true,
  }).on('change', async (e) => {

        $('#wicon').detach()
        $('#barcont').addClass('move')
        $('#cardstr').addClass('movediv')
        $('#cardstr').empty()
        
        let longitude = e.result.latlng.lng
        let latitude = e.result.latlng.lat
        let place = e.result.value
        let countrycode = e.result.countryCode

        console.log ('lat', latitude)
        console.log ('lon', longitude)
        console.log ('place', place)
        console.log ('country code', countrycode)




        let resp = await axios.post('/weather', {
        latitude : latitude,
        longitude : longitude,
        countrycode : countrycode
    })
    
    

    addData(place, resp)
    newshandle('headlines', countrycode)

    })

}

//Functions --------------------------------------------------

//add weather data to weather widget 
function addData (place, data){

    console.log('datttttta',data)
    
    loca.text(place)
    wind.text(data.data.wind.speed)
    temperature.text(data.data.main.temp)
    humidity.text(data.data.main.humidity)
    status.text(data.data.weather[0].description)
    let lilicon = data.data.weather[0].icon
    icon.append(`<img id= 'wicon' src=http://openweathermap.org/img/wn/${lilicon}.png alt="">`)

}

    
//function to get and handle news and append to the DOM
async function newshandle(headlines, contcode){

    let newsresp = await axios.get(`/${headlines}/${contcode}`)
    newsarray = newsresp.data.articles.splice(1, 16)
     return newsarray.forEach(story => {
      
      
   
     let containercard = $(`<div id='storycard' class="card mx-1 my-1" style="width: 15rem border-0"></div>`)
      let imgcard;
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
        $('#cardstr').append(card)
      }
      else {
        cardbody = cardboddiv.append(cardt,cardp, carda )
        card = containercard.append(imgcard, cardbody)
        return $('#cardstr').append(card)

      }
      

    })
}
















