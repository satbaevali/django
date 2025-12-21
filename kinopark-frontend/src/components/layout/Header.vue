
<script>
import { useRouter } from "vue-router";


export default{
    
    data(){
        return{
            movie:"Фильмы",
            headercinema:"Кинотеатры",
            food:"Еда и напитки",
            mykinopark:"Мой Kinopark",

            todayInKino:"Сегодня в кино",
            pre_sales:"Предпродажи",
            soon:"Скоро",
            isMovieVisiable:false, 
        }
    },
    setup(){
        const router = useRouter()

        function goToTodayInKino(){
        router.push('/today')
        }
        return{goToTodayInKino}
    },
    methods:{
        ShowMovie(){
            this.isMovieVisiable = true
        },
        HidenMovie(){
            this.isMovieVisiable = false
        },

    }
}
</script>

<template>
    <header>
        <div class = "header_part">
            <div class="container">
                <img src="../assets/img/logos.svg" alt="Kinopaark_logo">
                <div class="header">
                    <ul class="header_menu">
                        <li class="header_menu_item" @mouseout="ShowMovie" @mouseleave="HidenMovie">
                            <span>{{movie}}</span>
                            <div class="movieMenu"v-if="isMovieVisiable">
                                <div class="movieSchedule">
                                    <a href="">   
                                        <button class="movieVariant" @click="goToTodayInKino" >{{todayInKino}}</button>
                                    </a>
                                </div>
                                <div class="movieSchedule">
                                    <a href="">
                                        <button class="movieVariant">{{pre_sales}}</button>
                                    </a>
                                </div>
                                <div class="movieSchedule">
                                    <a href="">
                                        <button class="movieVariant">{{soon}}</button>
                                    </a>
                                </div>
                            </div>
                        </li>
                        <li class="header_menu_item"><span>{{headercinema}}</span></li>
                        <li class="header_menu_item"><span>{{food}}</span></li>
                        <li class="header_menu_item"><span>{{mykinopark}}</span></li>
                    </ul>
                    <div class="lan">
                        <div class="language">Рус</div>
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>

<style>
*{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body{
    margin: 0;
    padding: 0;
    font-family: Open Snas, sans-serif;
}
.header_part{
    box-shadow: 0 2px 8px rgba(0, 0, 0, .32);
    background-color: #fff;
    position:fixed;
    top:0;
    width:100%;
    z-index:101;
    padding-left:0;
    padding-right: 0;

}
.container{
    height:64px;
    display: flex;
    justify-content: space-between;
    max-width: 1240px;
    margin-left: auto;
    margin-right: auto;
    align-items: center;
    position: relative;

}
.container img{
    margin-top: 8px !important;
    display: inline-block;
    font-weight: 700;
    text-align: center;
    white-space: nowrap;
    width:120px;
}
.header{
    width:75%;
    justify-content: space-between;
    display: flex;
    align-items: center;
    height: 100%;
    position: static;
}
.header_menu{
    display: flex !important;
    height: 64px;
    padding: 0;
}
.header_menu_item{
    padding: 0 12px;
    cursor: pointer;
    margin-bottom: 2px;
}
.header ul{
    font-size: 1rem;
    font-weight: 500;
    margin-block-start: 1em;
    margin-block-end: 1em;
    padding-inline-start: 40px;
    unicode-bidi: isolate;
    list-style: none;
}
li {
    display: list-item;
    text-align: -webkit-match-parent;
    unicode-bidi: isolate;
}
li span{
    font-weight: 700;
    font-size: 1rem;
    color:#0e0e0e;
    line-height: 64px;
    padding-bottom: 21px;
    font-size: 16px;

}
li span:hover{
    color: #f96060;
    text-decoration:underline;
    text-underline-offset:25px;
}
.lan{
    margin-left: 3rem !important;
    align-items: center;
}
.language{
    font-weight: 700;
    font-size: 1rem;
}
.movieMenu{
    position: absolute;
    margin-left: -48px;
    z-index:999;
    display: block;
    background-color: #fff;
    opacity:1;
    box-shadow: 0 2px 8px rgba(0,0,0,.32);
    border-radius: 3px;
    
}
.movieSchedule{
    width:220px;
    height:100%;
    padding:8px 16px;
    cursor: pointer;
}
.movieVariant{
    border-radius:0;
    border:0;
    display: inline-block;
    font-weight: 500;
    text-align: center;
    white-space: nowrap;
    padding: 8px 16px;
    cursor: pointer;
    font-size:1rem;
}
</style>