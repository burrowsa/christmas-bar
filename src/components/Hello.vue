<template>
  <h1>{{ state.greeting }} {{ $route.params.who }}</h1>
</template>

<script>
import state from '@/components/shared'

export default {
  name: 'Hello',
  data () {
    return {
      state
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
