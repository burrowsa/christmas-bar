/*
Based on https://github.com/smronju/vue-webcam which unfortunately wouldn't compile
when I did npm run build - couldn't work out why but bringing it into the project
and tidying it up a bit got it working for me.

I've since extended it to support choosing which camera to use
*/

<template>
<div>
  <select v-model="camera" v-if="cameras.length > 1">
    <option v-for="camera of cameras" :value="camera.deviceId">{{ camera.label }}</option>
  </select>

  <video :width="width" ref="video" :height="height" :src="src" :autoplay="autoplay"></video>
</div>
</template>

<script>
export default {
  props: {
    autoplay: {
      type: Boolean,
      default: true
    },
    width: {
      type: Number,
      default: 300
    },
    height: {
      type: Number,
      default: 300
    },
    screenshotFormat: {
      type: String,
      default: 'image/jpeg'
    }
  },

  data () {
    return {
      src: '',
      stream: '',
      hasUserMedia: false,
      camera: null
    }
  },

  computed: {
    cameras () {
      const retval = []
      if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
        navigator.mediaDevices.enumerateDevices().then((deviceInfos) => {
          for (var deviceInfo of deviceInfos) {
            if (deviceInfo.kind === 'videoinput') {
              retval.push(deviceInfo)
            }
          }
          // This unexpected side-effect is a bit naughty I suppose but it works
          if (retval.length > 0 && this.camera == null) {
            this.camera = this.cameras[this.cameras.length - 1].deviceId
          }
        })
      }
      return retval
    }
  },

  methods: {
    getPhoto () {
      if (!this.hasUserMedia) return null

      const canvas = this.getCanvas()
      return canvas.toDataURL(this.screenshotFormat)
    },
    getCanvas () {
      if (!this.hasUserMedia) return null

      const video = this.$refs.video
      if (!this.ctx) {
        const canvas = document.createElement('canvas')
        canvas.height = video.clientHeight
        canvas.width = video.clientWidth
        this.canvas = canvas

        this.ctx = canvas.getContext('2d')
      }

      const { ctx, canvas } = this
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

      return canvas
    }
  },

  watch: {
    camera () {
      if (this.src) {
        this.beforeDestroy()
      }

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { deviceId: { exact: this.camera }, width: 300, height: 300 } }).then((stream) => {
          this.src = window.URL.createObjectURL(stream)
          this.stream = stream
          this.hasUserMedia = true
        }).catch(console.error)
      }
    }
  },

  beforeDestroy: function () {
    this.$refs.video.pause()
    this.src = ''
    this.stream.getTracks()[0].stop()
  }
}
</script>
