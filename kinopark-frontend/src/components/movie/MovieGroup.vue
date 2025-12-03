
<template>
      <div class="movie">
        <div class="movies-list" 
          v-for="movie in movies1"
          :key="movie.id"
          @click="$emit('toggle-detail',movie)"
          >
          <div class="img-movie">
            <img :src="movie.pictures" alt=""/>
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
        </div>
      </div>
</template>

<script>
export default {
  props:{
    movies1:Array,
    detail:Object
  }
}
</script>

<style>
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
</style>
