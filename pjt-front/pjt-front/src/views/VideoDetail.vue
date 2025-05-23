<template>
  <div class="container py-4">
    <button class="btn btn-link mb-3" @click="$router.back()">
      ← 뒤로가기
    </button>
    <div v-if="video" class="video-detail">
      <h2 class="mb-3">{{ video.snippet.title }}</h2>
      <p class="text-muted mb-4">
        업로드 날짜: {{ video.snippet.publishedAt | formatDate }}
      </p>
      <div class="ratio ratio-16x9 mb-4">
        <iframe
          :src="`https://www.youtube.com/embed/${video.id}`"
          title="YouTube video player"
          allowfullscreen
        ></iframe>
      </div>
      <p v-html="video.snippet.description"></p>
    </div>
    <div v-else class="text-center text-muted">
      로딩 중…
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VideoDetail',
  data() {
    return {
      video: null,
      isSaved: false
    }
  },
  async created() {
    const id = this.$route.params.id
    // 1) 상세 정보 가져오기
    const { data } = await axios.get(
      'https://www.googleapis.com/youtube/v3/videos', {
        params: {
          key: import.meta.env.VITE_YOUTUBE_API_KEY,
          part: 'snippet,statistics',
          id
        }
      }
    )
    this.video = data.items[0]
  },
  filters: {
    formatDate(value) {
      return new Date(value).toLocaleDateString()
    }
  },
  
}
</script>

<style scoped>
.video-detail h2 {
  word-break: keep-all;
}
.video-detail p {
  white-space: pre-wrap;
}
</style>
