import Home from "@/views/Home.vue";
import MovieList from "@/views/MovieList.vue";
import SchuldeMovie from "@/views/SchuldeMovie.vue";
import UnderHeader from "@/components/layout/UnderHeader.vue";
import { createRouter,createWebHistory } from "vue-router";


const routes = [
    {
    path:'/',
    name:'Home',
    component:Home,
    },
    {path:'/today',name:'Today',component:MovieList},
    {path:'/underheader', name:'UnderHeader',component:UnderHeader},
    {path:'/schulde/:id',name:'SculdeMovie',component:SchuldeMovie}
    
]

const router = createRouter({
    history:createWebHistory(),routes,
})

export default router