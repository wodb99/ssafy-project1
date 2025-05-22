<!-- <template>
  <div class="map-container">
    <div class="controls">
      <select v-model="selectedSido" @change="onSidoChange">
        <option value="">시/도를 선택하세요</option>
        <option v-for="s in mapInfo" :key="s.name" :value="s.name">{{ s.name }}</option>
      </select>
      <select v-model="selectedSigungu" @change="onSigunguChange" :disabled="!sigunguList.length">
        <option value="">시/군/구를 선택하세요</option>
        <option v-for="g in sigunguList" :key="g" :value="g">{{ g }}</option>
      </select>
      <select v-model="selectedBank" :disabled="!bankList.length">
        <option value="">은행을 선택하세요</option>
        <option v-for="b in bankList" :key="b" :value="b">{{ b }}</option>
      </select>
      <button @click="displayMarkers" :disabled="!selectedBank">찾기</button>
    </div>
    <div id="map" class="map"></div>
    <div v-if="showMessage" class="message">검색 결과를 클릭하세요.</div>
  </div>
</template>

<script>
import config from '@/config/apikey.js'
import mapData from '@/data/data.json'

export default {
  name: 'MapView',
  data() {
    return {
      map: null,
      ps: null,
      markers: [],
      destInfo: null,

      mapInfo: mapData.mapInfo,
      bankInfo: mapData.bankInfo,
      sigunguList: [],
      bankList: [],

      selectedSido: '',
      selectedSigungu: '',
      selectedBank: '',
      showMessage: false,
    }
  },
  methods: {
    async loadKakaoSDK() {
      if (window.kakao && window.kakao.maps) return
      return new Promise((resolve, reject) => {
        const script = document.createElement('script')
        script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${config.KAKAO_KEY}&libraries=services`
        script.async = true
        script.onload = resolve
        script.onerror = reject
        document.head.appendChild(script)
      })
    },
    initMap() {
      // 지도 초기화
      const center = new kakao.maps.LatLng(37.49818, 127.027386)
      this.map = new kakao.maps.Map(this.$el.querySelector('#map'), { center, level: 3 })
      this.ps = new kakao.maps.services.Places(this.map)

      // InfoWindow 설정 (목적지 표시용)
      this.destInfo = new kakao.maps.InfoWindow({ removable: true })
    },
    onSidoChange() {
      this.selectedSigungu = ''
      this.sigunguList = []
      this.bankList = []
      this.selectedBank = ''
      this.showMessage = false
      const region = this.mapInfo.find(x => x.name === this.selectedSido)
      if (!region) return
      this.sigunguList = [...region.countries]
    },
    onSigunguChange() {
      this.selectedBank = ''
      this.bankList = this.selectedSigungu ? [...this.bankInfo] : []
      this.showMessage = false
    },
    clearMarkers() {
      this.markers.forEach(obj => obj.marker.setMap(null))
      this.markers = []
    },
    clearInfos() {
      if (this.destInfo) this.destInfo.close()
    },
    displayMarkers() {
      if (!this.ps) {
        alert('지도가 아직 초기화되지 않았습니다. 잠시 후 다시 시도해 주세요.')
        return
      }
      this.showMessage = true
      this.clearMarkers()
      this.clearInfos()

      const query = `${this.selectedSido} ${this.selectedSigungu} ${this.selectedBank}`
      this.ps.keywordSearch(query, (places, status) => {
        if (status !== kakao.maps.services.Status.OK) return
        const bounds = new kakao.maps.LatLngBounds()
        places.forEach(p => {
          const pos = new kakao.maps.LatLng(p.y, p.x)
          const m = new kakao.maps.Marker({ map: this.map, position: pos })
          this.markers.push({ marker: m, place: p })
          bounds.extend(pos)
          // 마커 클릭 시 InfoWindow만 표시
          kakao.maps.event.addListener(m, 'click', () => {
            this.clearInfos()
            const infoStyle = `
              white-space:nowrap;
              text-align:center;
              padding:8px;
            `
            this.destInfo.setContent(`<div style="${infoStyle}"><strong>${p.place_name}</strong></div>`)
            this.destInfo.open(this.map, m)
          })
        })
        this.map.setBounds(bounds)
      })
    }
  },
  async mounted() {
    await this.loadKakaoSDK()
    this.initMap()
  }
}
</script>

<style scoped>
.map-container { display: flex; flex-direction: column; gap: 1rem; }
.controls select,
.controls button { margin-right: 0.5rem; padding: 0.5rem; }
#map { width: 100%; height: 500px; }
.message { margin-top: 0.5rem; color: #555; }
</style> -->

<template>
  <div class="map-container">
    <div class="controls">
      <select v-model="selectedSido" @change="onSidoChange">
        <option value="">시/도를 선택하세요</option>
        <option v-for="s in mapInfo" :key="s.name" :value="s.name">{{ s.name }}</option>
      </select>
      <select v-model="selectedSigungu" @change="onSigunguChange" :disabled="!sigunguList.length">
        <option value="">시/군/구를 선택하세요</option>
        <option v-for="g in sigunguList" :key="g" :value="g">{{ g }}</option>
      </select>
      <select v-model="selectedBank" :disabled="!bankList.length">
        <option value="">은행을 선택하세요</option>
        <option v-for="b in bankList" :key="b" :value="b">{{ b }}</option>
      </select>
      <button @click="displayMarkers" :disabled="!selectedBank">찾기</button>
    </div>
    <div class="map-detail-wrapper">
      <div id="map" class="map"></div>
      <!-- 오른쪽 상세 패널 -->
      <div class="detail-panel" v-if="selectedPlace">
        <h3>{{ selectedPlace.place_name }}</h3>
        <p>주소: {{ selectedPlace.road_address_name || selectedPlace.address_name }}</p>
        <p v-if="selectedPlace.phone">전화번호: {{ selectedPlace.phone }}</p>
        <a :href="selectedPlace.place_url" target="_blank">상세보기</a>
      </div>
    </div>
    <div v-if="showMessage" class="message">검색 결과를 클릭하세요.</div>
  </div>
</template>

<script>
import config from '@/config/apikey.js'
import mapData from '@/data/data.json'

export default {
  name: 'MapView',
  data() {
    return {
      map: null,
      ps: null,
      markers: [],
      destInfo: null,

      mapInfo: mapData.mapInfo,
      bankInfo: mapData.bankInfo,
      sigunguList: [],
      bankList: [],

      selectedSido: '',
      selectedSigungu: '',
      selectedBank: '',
      selectedPlace: null,   // 클릭된 지점 정보
      showMessage: false,
    }
  },
  methods: {
    async loadKakaoSDK() {
      if (window.kakao && window.kakao.maps) return
      return new Promise((resolve, reject) => {
        const script = document.createElement('script')
        script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${config.KAKAO_KEY}&libraries=services`
        script.async = true
        script.onload = resolve
        script.onerror = reject
        document.head.appendChild(script)
      })
    },
    initMap() {
      const center = new kakao.maps.LatLng(37.49818, 127.027386)
      this.map = new kakao.maps.Map(this.$el.querySelector('#map'), { center, level: 3 })
      this.ps = new kakao.maps.services.Places(this.map)
      this.destInfo = new kakao.maps.InfoWindow({ removable: true })
    },
    onSidoChange() {
      this.selectedSigungu = ''
      this.sigunguList = []
      this.bankList = []
      this.selectedBank = ''
      this.selectedPlace = null
      this.showMessage = false
      const region = this.mapInfo.find(x => x.name === this.selectedSido)
      if (!region) return
      this.sigunguList = [...region.countries]
    },
    onSigunguChange() {
      this.selectedBank = ''
      this.bankList = this.selectedSigungu ? [...this.bankInfo] : []
      this.selectedPlace = null
      this.showMessage = false
    },
    clearMarkers() {
      this.markers.forEach(obj => obj.marker.setMap(null))
      this.markers = []
    },
    clearInfos() {
      if (this.destInfo) this.destInfo.close()
      this.selectedPlace = null
    },
    displayMarkers() {
      if (!this.ps) {
        alert('지도가 아직 초기화되지 않았습니다.')
        return
      }
      this.showMessage = true
      this.clearMarkers()
      this.clearInfos()

      const query = `${this.selectedSido} ${this.selectedSigungu} ${this.selectedBank}`
      this.ps.keywordSearch(query, (places, status) => {
        if (status !== kakao.maps.services.Status.OK) return
        const bounds = new kakao.maps.LatLngBounds()
        places.forEach(p => {
          const pos = new kakao.maps.LatLng(p.y, p.x)
          const m = new kakao.maps.Marker({ map: this.map, position: pos })
          this.markers.push({ marker: m, place: p })
          bounds.extend(pos)
          kakao.maps.event.addListener(m, 'click', () => {
            this.clearInfos()
            this.selectedPlace = p
          })
        })
        this.map.setBounds(bounds)
      })
    }
  },
  async mounted() {
    await this.loadKakaoSDK()
    this.initMap()
  }
}
</script>

<style scoped>
.map-container { display: flex; flex-direction: column; gap: 1rem; }
.controls select,
.controls button { margin-right: 0.5rem; padding: 0.5rem; }
.map-detail-wrapper { display: flex; }
#map { flex: 1; height: 500px; }
.detail-panel { width: 300px; padding: 1rem; border-left: 1px solid #ddd; background: #fafafa; overflow-y: auto; }
.message { margin-top: 0.5rem; color: #555; }
</style>