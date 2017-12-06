<template>
  <a href="#" class="upload btn btn-default glyphicon glyphicon-upload">
    <input type="file" class="opacity" v-on:change="loadFile" accept="image/*"></input>
  </a>
</template>

<script>
export default {
  name: 'ImageUpload',
  data () {
    return {
    }
  },

  props: {
    width: {
      type: Number,
      default: 300
    },
    height: {
      type: Number,
      default: 300
    },
    format: {
      type: String,
      default: 'image/jpeg'
    }
  },

  methods: {
    loadFile (event) {
      const file = event.target.files[0]

      if (!file.type.includes('image/')) {
        this.$toast('Please select an image', {
          className: 'et-info',
          horizontalPosition: 'center'
        })
        return
      }

      const reader = new FileReader()
      reader.onload = (e) => {
        const image = new Image()
        image.onload = () => {
          let width = image.width
          let height = image.height

          if (width > this.width || height > this.height) {
            if (width > height) {
              height = this.width * (height / width)
              width = this.width
            } else {
              width = this.height * (width / height)
              height = this.height
            }
          }

          const canvas = document.createElement('canvas')
          const context = canvas.getContext('2d')
          canvas.width = width
          canvas.height = height
          context.drawImage(image, 0, 0, width, height)

          this.$emit('image', canvas.toDataURL(this.format))
        }
        image.src = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }
}
</script>


<style>
.upload input[type="file"]{
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
}
.opacity{
   -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";
    filter: alpha(opacity=0);
   -moz-opacity: 0;
   -khtml-opacity: 0;
   opacity: 0;
}
</style>
