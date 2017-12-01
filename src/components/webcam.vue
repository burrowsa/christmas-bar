/*
Based on https://github.com/smronju/vue-webcam which unfortunately wouldn't compile
when I did npm run build - couldn't work out why but bringing it into the project
and tidying it up a bit got it working for me.
*/

<template>
<video :width="width" ref="video" :height="height" :src="src" :autoplay="autoplay"></video>
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
      default: 400
    },
    height: {
      type: Number,
      default: 300
    },
    mirror: {
      type: Boolean,
      default: true
    },
    screenshotFormat: {
      type: String,
      default: 'image/jpeg'
    }
  },

  data () {
    return {
      video: '',
      src: '',
      stream: '',
      hasUserMedia: false,
      styleObject: {
        transform: 'scale(-1, 1)',
        filter: 'FlipH'
      }
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

          /* if (this.mirror) {
           const context = canvas.getContext('2d')
           context.translate(canvas.width, 0)
           context.scale(-1, 1)
           this.ctx = context
           } else {
           this.ctx = canvas.getContext('2d')
           } */
      }

      const { ctx, canvas } = this
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

      return canvas
    }
  },

  mounted: function () {
    this.video = this.$refs.video
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia

    if (navigator.getUserMedia) {
      navigator.getUserMedia({ video: true }, (stream) => {
        this.src = window.URL.createObjectURL(stream)
        this.stream = stream
        this.hasUserMedia = true
      }, (error) => {
        console.log(error)
      })
    }
  },

  beforeDestroy: function () {
    this.video.pause()
    this.src = ''
    this.stream.getTracks()[0].stop()
  },

  destroyed: function () {
    console.log('Destroyed')
  }
}
</script>
