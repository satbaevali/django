<!-- src/views/Home.vue -->
<script>
import UnderHeader from '@/components/layout/UnderHeader.vue'
import MovieGroup from '@/components/movie/MovieGroup.vue'
import DetailMovie from '@/components/movie/DetailMovie.vue'
import SoonMovie from '@/views/SoonMovie.vue'
import MyCinema from '@/views/MyCinema.vue'

export default {
  components: {
    UnderHeader,
    MovieGroup,
    DetailMovie,
    SoonMovie,
    MyCinema
  },
  data() {
    return {
      hidden_movie: true,
      hidden_movie1: false,
      movies: [
        {
          id: 1,
          name: "Сыныптас",
          ganre: ['драма', 'комедия'],
          pictures: "https://i.ibb.co/Y76XZ5BV/Whats-App-2025-10-13-15-11-25-c8f72724.webp",
          age: "18+",
          duration: "2ч 10м",
          country: "Казахстан",
          discription: "После долгих лет разлуки двое бывших одноклассников случайно встречаются на встрече выпускников. Вспоминая школьные годы, они понимают, что многое изменилось, но чувства остались прежними.",
        },
        {
          id: 2,
          name: "Капитан Байтасов",
          ganre: ['экшн', 'драма'],
          pictures: "https://i.ibb.co/bM1rDs6m/Whats-App-2025-10-06-17-13-32-5cdd521c.webp",
          age: "16+"
        },
        {
          id: 3,
          name: "Әкеңнің баласы",
          ganre: ['экшн', 'комедия'],
          pictures: "https://i.ibb.co/h1V5WCWq/image-2025-10-02-T111708-033.webp",
          age: "14+"
        },
        {
          id: 4,
          name: "Изумительная Мокси",
          ganre: ['мультфильм', 'комедия', 'приключения'],
          pictures: "https://i.ibb.co/xKWWx4b3/image-2025-09-30-T164318-471.webp",
          age: "6+"
        },
        {
          id: 5,
          name: "Ыстық ұя",
          ganre: ['драма'],
          pictures: "https://i.ibb.co/84d7TmnB/100-70.webp",
          age: "14+"
        },
        {
          id: 6,
          name: "Бақыт құшағында",
          ganre: ['мюзикл', 'романтическая ', 'комедия'],
          pictures: "https://i.ibb.co/84GnqxJ8/Whats-App-2025-10-01-11-24-14-cca049fa.webp",
          age: "14+"
        },
        {
          id: 7,
          name: "Болған оқиға",
          ganre: ['драма', 'комедия'],
          pictures: "https://i.ibb.co/JF5BbMmB/image.png",
          age: "14+"
        },
        {
          id: 8,
          name: "Трон Арес",
          ganre: ['фантастика', 'боевик'],
          pictures: "https://i.ibb.co/QjpNSfKV/Whats-App-2025-10-06-11-00-10-e0a59b8b.webp",
          age: "18+"
        },
      ],
      detailGroup1: null,
      detailGroup2: null,
    }
  },
  methods: {
    SoonKino() {
      this.hidden_movie = false
      this.hidden_movie1 = true
    },
    TodayKino() {
      this.hidden_movie = true
      this.hidden_movie1 = false
    },
    toggleDetail(group, movie) {
      if (group === 1) {
        this.detailGroup2 = null
        this.detailGroup1 = this.detailGroup1 && this.detailGroup1.id === movie.id ? null : movie
      } else if (group === 2) {
        this.detailGroup1 = null
        this.detailGroup2 = this.detailGroup2 && this.detailGroup2.id === movie.id ? null : movie
      }
    }
  }
}
</script>

<template>
  <div>
    <!-- Подхедер с фильтрами -->
    <div class="under-header">
      <UnderHeader />
    </div>

    <!-- Рекламный баннер -->
    <div class="advertising-slider-wrapper"></div>

    <!-- Основной контент -->
    <section class="section">
      
      <!-- Секция "Сегодня в кино" -->
      <div class="section_content" v-show="hidden_movie">
        <div class="section_header">
          <p class="header_text1">Сегодня в кино</p>
          <p class="header_text3" @click="SoonKino">Скоро на экранах</p>
          <div class="ml-auto">
            <p class="text3">Смотреть расписание всех кинотеатров</p>
          </div>
        </div>

        <div class="general-movie">
          <MovieGroup
            :movies1="movies.slice(0, 4)"
            @toggle-detail="toggleDetail(1, $event)"
            :detail="detailGroup1"
          />
          <div class="detail" v-if="detailGroup1">
            <DetailMovie :movie="detailGroup1" />
          </div>
          <MovieGroup
            :movies1="movies.slice(4)"
            @toggle-detail="toggleDetail(2, $event)"
            :detail="detailGroup2"
          />
          <div class="detail" v-if="detailGroup2">
            <DetailMovie :movie="detailGroup2" />
          </div>
        </div>

        <div class="Schulde">
          <button>
            <router-link to="/today">Посмотреть все фильмы</router-link>
          </button>
        </div>
      </div>

      <!-- Секция "Скоро на экранах" -->
      <div class="section_content" v-show="hidden_movie1">
        <SoonMovie @soon-in-today="TodayKino" />
      </div>

      <!-- Секция "Мой Kinopark" -->
      <div class="section_content">
        <MyCinema />
      </div>

    </section>
  </div>
</template>

<style>
.section {
  padding: 36px 0;
}

.section_content {
  max-width: 1240px;
  margin: 0 auto;
  padding: 36px 0;
  font-family: Open Sans, sans-serif;
}

.section_header {
  max-width: 1240px;
  margin: 0 auto;
  display: flex;
  font-family: Open Sans, sans-serif;
}

.header_text1 {
  font-size: 36px;
  font-weight: 700;
  margin-right: 20px;
  cursor: pointer;
}

.header_text3 {
  color: rgb(140, 141, 147);
  font-weight: 400;
  font-size: 36px;
  border-left-color: rgb(195, 29, 40);
  border-left-style: solid;
  border-left-width: 1.6px;
  padding-left: 20px;
  cursor: pointer;
}

.ml-auto {
  margin-left: auto;
  font-size: 13px;
  font-weight: 400;
}

.under-header {
  background-color: #3e454b;
  align-items: center;
  height: 82px;
  color: rgb(14, 14, 14);
  display: flex;
  margin-top: 64px;
}

.advertising-slider-wrapper {
  width: 1440px;
  height: 320px;
  margin: auto;
  background: url(https://i.ibb.co/vvzHj1sh/1440x320-kb-kopi.jpg);
}

.general-movie {
  width: 100%;
  margin-top: 32px;
}

.movie {
  display: flex;
  flex-wrap: wrap;
  row-gap: 2%;
  column-gap: 2%;
}

.Schulde button {
  padding: 8px 36px;
  border-radius: 3px;
  border: 0;
  background-color: #c31d28;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.Schulde {
  text-align: center;
}

.Schulde a {
  color: #fff;
}
</style>