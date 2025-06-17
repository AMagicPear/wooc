<script setup lang="ts">
import Card from 'primevue/card'
</script>

<template lang="pug">
.notice
    Card()
        template(#title) 课程公告
        template(#content)
            p.m-0 课程公告内容
</template>

<style lang="css" scoped>
.notice{
    margin-top: 20px;
}
</style>