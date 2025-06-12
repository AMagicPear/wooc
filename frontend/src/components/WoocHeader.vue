<template>
    <header>
        <router-link to="/" class="left">
            <img src="@/assets/pic/wooc-logo.png" />
            <h2>→砖大学WOOC</h2>
        </router-link>
        <nav>
            <router-link to="/">首页</router-link>
            <router-link to="/about">关于</router-link>
            <router-link to="/login">登录｜注册</router-link>
        </nav>
    </header>
</template>

<style lang="css" scoped>
.left{
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: bold;
}

a.left{
    text-decoration: none;
    color: var(--color-text);
}

.left>img{
    width: 40px;
}
nav {
    display: flex;
    gap: 15px;
}

nav a {
    text-decoration: none;
    color: var(--color-text);
}

header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: var(--color-background);
    color: var(--color-text);
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
    padding: 15px 20px;
    height: 60px;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
</style>