<template>
<div class="movie-container">
    <div class="left-router">
      <p class="a1"><a href="/">Главная /</a></p>
      <p class="a1"><a href="">Фильмы</a></p>
      <p class="a2"><a href="/schulde">{{movie.name}}</a></p>
    </div>
</div>
</template>

<script>
export default{
    props:{
        movie:Object
    }
}
</script>

<style>
.movie-container{
  max-width:1240px;
  margin: 0 auto;
  display: block;
  box-sizing: border-box;
  font-family: Open Sans,sans-serif;
  margin-top:64px;
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
</style>
