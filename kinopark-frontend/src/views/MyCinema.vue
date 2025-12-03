
<script>
export default{
    data(){
        return{
            cinemes:[
                {
                    id:1,
                    name:"IMAX",
                    pictures:"https://www.kinopark.kz/static/img/photos/imax-main1.jpg",
                    info:"Комплекс технологий, призванный обеспечить непревзойденное качество демонстрации фильмов",
                    viewinfo:false,
                },
                {
                    id:2,
                    name:"Hot Price",
                    pictures:"https://www.kinopark.kz/static/img/photos/hotprice1.jpg"
                },
                {
                    id:3,
                    name:"Premium",
                    pictures:"https://www.kinopark.kz/static/img/photos/firstclass1.jpg"

                },
                {
                    id:4,
                    name:"Tiger Food",
                    pictures:"https://www.kinopark.kz/static/img/photos/tigerfood1.jpg"

                }
            ],
            
        }
    },
    methods:{
        ViewInfo(id){
           const cinema = this.cinemes.find(c => c.id === id);
           if(cinema) cinema.viewinfo = true

        },
        CloseInfo(id){
            const cinema = this.cinemes.find(c => c.id === id);
            if(cinema) cinema.viewinfo =false
        }
    }
}
</script>

<template>
        <div class="in-cinema">
            <p class="text-section">Mой Kinopark</p>
            <div class="ml-auto">
                <p class="view-all">Смотреть все</p>
            </div>
        </div>
        <div class="mycinema-content">
            <div class="my-cinema-list">
                <div class="my-cinema-item" v-for="cinema in cinemes":key="cinema.id">
                    <img :src= "cinema.pictures" alt="" class="img" @mouseenter="ViewInfo(cinema.id)" @mouseleave="CloseInfo(cinema.id)">
                    <div class="item-title">
                        <p>{{cinema.name}}</p>
                    </div>
                    <div class="item-title-info" v-if="cinema.viewinfo" >
                        <p class="item-title">{{cinema.name }}</p>
                        <div class="info"><p class="in-info">{{cinema.info }}</p></div>
                    </div>
                </div>
            </div>
        </div>
</template>

<style>

.in-cinema{
    display: flex;
    margin-bottom: 32px;
}
.text-section{
   font-size: 2.25rem;
   font-weight: 700;
   color:rgb(55, 61, 63);
}
.mycinema-content{
    width:100%;
}
.my-cinema-list{
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap:16px;
    
}
.my-cinema-item{
    position: relative;
    width: calc(33.33333% - 17.33333px);
    height:207px;
    margin-bottom: 24px;
    display: block;
    cursor: pointer;
    
}
.img{
    height:100%;
    width: 100%;
    border-radius: 3px;

}
.item-title{
    position: absolute;
    bottom:12px;
    left: 12px;
    color:#fff;
}

.item-title p{
    font-size: 24px;
    font-weight: 700;
}

</style>