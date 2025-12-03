<template>
    <div class="detail-movie">
        <div class="detail-container">
            <div class="detail-movie-video-and-description">
                <div class="desciption">
                    <div class="name-movie1">
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
                    <div class="duration-and-des" v-if="movie.duration && movie.country && movie.discription">
                        <p><strong>Продолжительность:</strong> {{movie.duration}}</p>
                        <p><strong>Страна:</strong> {{movie.country}}</p>
                        <p class="description">{{movie.discription}}</p>
                        <button type="button" class="Button" @click="openShulde">Смотреть расписание</button>
                    </div> 
                </div>
            </div>
            <div class="video">
                  <iframe frameborder="1" modestbranding=1 rel="0" controls="0" showinfo="0" allowfullscreen  allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
                  gyroscope; picture-in-picture; web-share" title="Cыныптас | Synyptas | Ресми Трейлер (2025)" referrerpolicy="strict-origin-when-cross-origin" width="100%" height="100%"
                  src="https://www.youtube.com/embed/LYyHpfTtwUA?autoplay=1&mute=0&controls=0&origin=https%3A%2F%2Fwww.
                  kinopark.kz&playsinline=1&showinfo=0&rel=0&iv_load_policy=3&modestbranding=1&ecver=2&enablejsapi=1&widgetid=3&forigin=https%3A%2F%2Fwww.
                  kinopark.kz%2Fru&aoriginsup=1&gporigin=https%3A%2F%2Fwww.kinopark.kz%2Fru%2Fmovies%2Ftoday&vf=1"
                  ></iframe>
                </div>
        </div>
    </div>
</template>

<script>

import SchuldeMovie from '@/views/SchuldeMovie.vue';


export default{

    components:{SchuldeMovie},
    props:{
      movie:Object
    },
    methods: {
        openShulde(){
            this.$router.push(`/schulde/${this.movie.id}`)
        }
    }
}
</script>

<style>
.detail-movie{
    max-width: 1240px;
    font-family: Open Sans, sans-serif;
}
.detail-container{
  max-width: 1240px;
  display: flex;
}
.detail-movie-video-and-description{
    display: flex;
    margin-bottom:28px;
    width:100%;
 }
.desciption{
  display: block;
  
}
.name-movie1{
    font-size: 24px;
    font-weight: 700;
    margin-bottom:8px;
    line-height: 33px;
}
.genre-age{
    display: flex;
    margin-top:4px;
    align-items:flex-start ;
}
.video{
 width:100%;
 clip-path: inset(0 0 0 10px round 3px);
 border-image: linear-gradient(90deg,#141414 4.25%,rgba(20,20,20,0));
}
iframe{
  width:100%;
  height:320px;
  scrollbar-width: none;
}
.duration-and-des{
    margin-top: 24px;
}
.description{
    margin-top: 24px;
}
.Button{
    margin-top: 24px;
    font-size: 13px;
    padding: 8px 16px;
    font-weight: 700;
    background-color: rgb(
    195, 29, 40);
    color: #fff;
    border: 0;
    border-radius: 3px;
}



</style>
