<script>

import { useRoute } from 'vue-router';

export default{
    data(){
        return{
            ShowCatalog:false,
            selectCity:"Алматы",
            cities:["Алматы","Астана","Шымкент","Нарынқол"],
            select:false,

            ShowCinema:false,
            selectCinema:"Выберите кинотеатр",
            cinemas:["KinoPark1","KinoPark2","KinoPark"],
            select1:false,
            selectedCinema:[],

            ShowMoviee:false,
            selectMovie:"Выберите фильм",
            movies:["Ыстық ұя","Әменгер","Таптым-ау сені","Сен"],
            selectedMovies:[],
            select2:false,

            cinmemaa:false,
        }
    },
    setup(){
        const router = useRoute

        function togoToday(){
            router.push('/today')
        }
        return{togoToday}
    },
    methods:{
        cinemaShow(){
            this.cinmemaa =! this.cinmemaa
        },
        toggleCityList(){
            this.ShowCatalog = !this.ShowCatalog
            this.ShowCinema = false,
            this.ShowMoviee = false
        },
        toggleCinemaList(){
            this.ShowCinema = !this.ShowCinema
            this.ShowCatalog=false
            this.ShowMoviee = false
        },
        toggleMovieList(){
            this.ShowMoviee = !this.ShowMoviee
            this.ShowCatalog=false,
            this.ShowCinema = false
        },
        selectCity(city){
            this.selectCity = city,
            this.ShowCatalog = false
        },
        selectCinema(cinema){
            if(this.selectedCinema.includes(cinema)){
                this.selectedCinema = this.selectedCinema.filter(c=>c !== cinema)
            }
            else{
                this.selectCinema.push(cinema)
            }
        },
        selectCinemaLength(){
            if(this.selectedCinema.length == 0){
                return selectCinema
            }
        },
        selectMovie(movie){
           if(this.selectedMovies.includes(movie)){
            this.selectedMovies = this.selectedMovies.filter(c=>c!== movie)
           }
           else{
            this.selectedMovies.push(movie)
           }
        },
        selectMovieLength(){
            if(this.selectedMovies.length == 0){
                return selectMovie
            }
        },
        checkedClose(city){
            this.selectCity = city,
            this.ShowCatalog = false
        },
        checkedCloseCinema(cinema){
            this.selectCinema=cinema,
            this.ShowCinema = false
        },
        checkedCloseMovie(movie){
            this.selectMovie = movie,
            this.ShowMoviee = false
        },
    }
}
</script>

<template>
    <div class="in-container">
            <div class="search">
                <button type="button" class="button" @click="toggleCityList">
                    <img src="../assets/img/map-marker-alt.svg" alt="map-market">
                    <div class="in-button">
                        <p class="insearch">{{ selectCity }}</p>
                    </div>
                    <img src="../assets/img/caretDownBlack.svg" alt="Downblack" class="left">
                </button>
                <ul v-if="ShowCatalog" class="Showcities">
                    <li class="cities">
                        <div v-for="city in cities" :key="city" class="selectCity">
                            <label class="checkbox-label"> <input 
                                type="radio" 
                                :value="city" 
                                v-model="selectCity" 
                                @change="toggleCityList" 
                                />
                            {{ city }}
                            </label>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="search">
                <button type="button" class="button" @click="toggleCinemaList">
                    <img src="../assets/img/cinema.svg" alt="5" class="cinema">
                    <div class="in-button">
                        <p v-if="selectedCinema.length === 0" class="insearch">{{selectCinema}}</p>
                        <p v-else class="insearch">Выбрано кинотеатров ({{selectedCinema.length}})</p>
                    </div>
                    <img src="../assets/img/caretDownBlack.svg" alt="Downblack" class="left1">
                </button>
                <ul v-if="ShowCinema" class="Showcities">
                    <li class="cities">
                        <button v-for="(cinema,i) in cinemas"
                            :key="i"
                            class="selectCity">  
                        <label class="checkbox">
                            <input type="checkbox" :value="cinema" v-model="selectedCinema">
                        </label>
                        {{ cinema }}
                        </button>
                    </li>
                </ul>
            </div>
            <div class="search">
                <button type="button" class="button" @click="toggleMovieList">
                    <img src="../assets/img/movie-circle.svg" alt="5">
                    <div class="in-button">
                        <p v-if="selectedMovies.length === 0" class="insearch">{{selectMovie}}</p>
                        <p v-else class="insearch">Выбрано фильмов ({{selectedMovies.length}})</p>
                    </div>
                    <img src="../assets/img/caretDownBlack.svg" alt="Downblack" class="left2">
                </button>
                <ul v-if="ShowMoviee" class="Showcities">
                    <li class="cities">
                        <button v-for="(movie,i) in movies"
                            :key="i"
                            class="selectCity">  
                        <label class="checkbox">
                            <input type="checkbox" :value="movie" v-model="selectedMovies">
                        </label>
                        {{ movie }}
                        </button>
                    </li>
                </ul>
            </div>
            <a href="">
                <div class="buyticket">Купить билеты</div>
            </a>
        </div>
        
</template>

<style>
.in-container{
    align-items: center;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 1240px;
    margin-left: auto;
    margin-right: auto;
    padding-top: 20px;
    padding-bottom: 20px;
    gap: 20px;
}
.search{
    width:100%;
    display: block;
    box-sizing: border-box;
    flex-basis: 19%;
    position: relative;
    flex-grow: 0;
    flex-shrink: 0;
    font-size: 16px;
    font-weight: 700;
    align-items: center;
}

.button{
    white-space: nowrap;
    align-items: center;
    background-clip: border-box;
    background-position-x: 0;
    background-position-y: 50%;
    display: flex;
    cursor: pointer;
    font-weight: 700;
    padding: 12px;
    border-radius: 3px;
    font-size: 16px;
    flex: 30%;
    border: 0;
}
.button:hover{
    background-color: #aaa;
}
.button img{
    margin-right:8px;
    width:16px;
    height: 16px;
}
.in-button{
    flex: 1;
    margin-right: 40px;

    
}
.left{
    margin-left: auto;
    width:12px;
    height:12px;
    margin-left: 60px;
}
.left1{
    margin-left: 90px;
    width:12px;
    height: 12px;
}
.left2{
    margin-left: 127px;
}
.buyticket{
    font-size: .8125rem;
    font-weight:700;
    line-height: 18px;
    background-color: #c31d28;
    color: #fff;
    padding: 12px 28px;
}
a{
    text-decoration: none;
}
.Showcities{
    max-width:404px;
    overflow-y:auto;
    width:100%;
    position: absolute;
    background-color: #fff;
    border-radius:3px;
    margin-top: 5px;
    z-index: 6;
    font-weight: 500;
    font-size: 1rem;
    font-family: Open Sans,sans-serif;
    display: block;

}
.Showcities ul{
    padding: 0px;
}
.cities button{
    border-bottom: 1px solid #ddd;
}
.selectCity{
    display: block;
    padding:0px 8px;
    width:100%;
    padding: 8px 16px 8px 7px;
    text-align: left;
    align-items: center;
    border-left: 5px solid #c31d28;
    line-height: 28px;

}

input:checked+ .mark{
    background-color: #c31d28;
}
.checkbox{
    position: relative;
    padding-left: 15px;
    cursor: pointer;
    font-size: 20px;
    padding-right: 3px;
}
.box::after{
    color: #c31d28;
}

</style>
