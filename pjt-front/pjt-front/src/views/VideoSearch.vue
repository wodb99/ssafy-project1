<template>
  <div class="container py-4">
    <button class="btn btn-link mb-3" @click="$router.back()">
      ← 뒤로가기
    </button>
    <h2 class="mb-4 text-center">비디오 검색</h2>
    <form @submit.prevent="searchVideos" class="input-group mb-4">
      <input
        v-model="query"
        type="text"
        class="form-control"
        placeholder="검색어를 입력하세요"
      />
      <button class="btn btn-success" type="submit">찾기</button>
    </form>

    <!-- 검색 결과 그리드 -->
    <div class="row g-4">
      <div
        v-for="video in videos"
        :key="video.id.videoId"
        class="col-sm-6 col-md-4"
      >
        <router-link
          :to="`/video/${video.id.videoId}`"
          class="text-decoration-none d-block h-100"
        >
          <div class="card h-100 video-card">
            <img
              :src="video.snippet.thumbnails.medium.url"
              class="card-img-top"
              :alt="video.snippet.title"
            />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title small text-dark">
                {{ video.snippet.title }}
              </h5>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- 검색 후 결과 없을 때 -->
    <div
      v-if="searched && videos.length === 0"
      class="text-center mt-5 text-muted"
    >
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script>
import axios from 'axios'

// .env에서 불러온 키
const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

export default {
  name: 'Home',
  data() {
    return {
      query: '',
      videos: [],
      searched: false,
    }
  },
  methods: {
    async searchVideos() {
      this.searched = false

      try {
        const { data } = await axios.get(
          'https://www.googleapis.com/youtube/v3/search',
          {
            params: {
              key: API_KEY,
              part: 'snippet',
              q: this.query,
              type: 'video',
              maxResults: 12,
            }
          }
        )
        this.videos = data.items
      } catch (e) {
        console.error(e)
        this.videos = []
      } finally {
        this.searched = true
      }
    }
  }
}
</script>

<style scoped>
.video-card {
  cursor: pointer;
  transition: transform .2s;
}
.video-card:hover {
  transform: scale(1.02);
}
.text-decoration-none {
  text-decoration: none !important;
}
.card-title {
  height: 3em;
  overflow: hidden;
}
</style>
