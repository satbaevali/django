

<script>
export default{
  data(){
    return{
      movies:[
        {
          id:1,
          name:"Сыныптас",
          ganre:['драма','комедия'],
          pictures:"https://i.ibb.co/Y76XZ5BV/Whats-App-2025-10-13-15-11-25-c8f72724.webp",
          age:"18+"
        },
        {
          id:2,
          name:"Капитан Байтасов",
          ganre:['экшн','драма'],
          pictures:"https://i.ibb.co/bM1rDs6m/Whats-App-2025-10-06-17-13-32-5cdd521c.webp",
          age:"16+"
        },
        {
          id:3,
          name:"Әкеңнің баласы",
          ganre:['экшн','комедия'],
          pictures:"https://i.ibb.co/h1V5WCWq/image-2025-10-02-T111708-033.webp",
          age:"14+"
        },
        {
          id:4,
          name:"Изумительная Мокси",
          ganre:['мультфильм', 'комедия', 'приключения'],
          pictures:"https://i.ibb.co/xKWWx4b3/image-2025-09-30-T164318-471.webp",
          age:"6+"
        },
        {
          id:5,
          name:"Ыстық ұя",
          ganre:['драма'],
          pictures:"https://i.ibb.co/84d7TmnB/100-70.webp",
          age:"14+"
        },
        {
          id:6,
          name:"Бақыт құшағында",
          ganre:['мюзикл', 'романтическая ','комедия'],
          pictures:"https://i.ibb.co/84GnqxJ8/Whats-App-2025-10-01-11-24-14-cca049fa.webp",
          age:"14+"
        },
        {
          id:7,
          name:"Болған оқиға",
          ganre:['драма','комедия'],
          pictures:"https://i.ibb.co/JF5BbMmB/image.png",
          age:"14+"
        },
        {
          id:8,
          name:"Трон Арес",
          ganre:['фантастика','боевик'],
          pictures:"https://i.ibb.co/QjpNSfKV/Whats-App-2025-10-06-11-00-10-e0a59b8b.webp",
          age:"18+"
        },
        
      ]
    }
  }
}
</script>

<template>
  <div class="movie-container">
    <div class="left-router">
      <p class="a1"><a href="/">Главная /</a></p>
      <p class="a2"><a href=""> Сегодня в кино</a></p>
    </div>
    <div>
      <h1 class="h1">Сегодня в кино</h1>
    </div>
    <div class="general-movie">
      <div class="movie">
        <div class="movies-list" v-for="movie in movies":key="movie.id">
          <div class="img-movie">
            <img :src="movie.pictures" alt="">
          </div>
          <div class="name-movie">
            <p>{{movie.name }}</p>
          </div>
          <div class="genre-age">
            <p>{{movie.ganre.join(', ')}}</p>
            <div class="sticker">
              <div class="in-sticker">
                <p class="age">{{movie.age}}</p>
              </div>
            </div>
          </div>
          <div class="movie-schulde">
            <button>Расписание</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style>
.movie-container{
  max-width:1240px;
  margin: 0 auto;
  display: block;
  box-sizing: border-box;
  font-family: Open Sans,sans-serif;
  margin-top:64px;
}

.general-movie{
  width:100%;
  margin-top: 32px;
}
.movie{
  display: flex;
  flex-wrap: wrap;
  gap:2%;
  
}
.movies-list{
  margin-bottom: 48px;
  display: flex;
  flex-direction:column;
  justify-content: center;
}
.name-movie{
  margin-top: 8px;
  font-size: 16px;
  font-weight: 700;
}

.genre-age{
  display: flex;
  margin-bottom: 16px;
  font-size: 13px;
  font-weight: 400;
}

.stciker{
  position: relative;
  min-width:24px;
  height: 24px;
  margin-left: 8px;
}
.in-sticker{
  position: absolute;
  width: 16px;
  height:16px;
  background:#ffd362;
  border-radius:2px;
  transform: rotate(45deg);
}
.age{
  transform: rotate(-45deg);
  font-size: .625rem;
  font-weight: 700;
}

.genre-age p{
  margin-top: 4px;
  width:75%;
}
.movies-list img{
  width:291.25px;
  height: 369px;
  border-radius: 3px;
  object-fit: cover;
}
.movie-schulde button{
  background-color: #c31d28;
  color: #fff;
  border: 0;
  padding: 8px 36px;
  text-align: center;
  border-radius: 3px;
}
.left-router{
  display: flex;
  padding: 24px 0;
}
.a2 a{
  text-decoration: none;
  color:#0e0e0e;
  padding-right:5px;
  font-weight: 700;
  margin-left:6px;
  font-size: 13px;
}
.a1 a{
  text-decoration: none;
  color:#0e0e0e;
  padding-right:5px;
  font-weight: 400;
  margin-left:6px;
  font-size: 13px;
}
.h1{
  font-size: 3.25rem;
  font-weight: 700;
}
</style>
