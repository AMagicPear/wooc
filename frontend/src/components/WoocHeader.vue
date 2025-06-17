<script setup lang="ts">
import { accountState } from "@/global/account";
import getBackgroundColor from "@/util/usernameBgColor";
import { Avatar } from "primevue";
import Menu from "primevue/menu";
import { computed, ref } from "vue";
const avatarMenu = ref();
const items = ref([
  {
    label: "个人信息",
    items: [
      {
        label: "个人主页",
        icon: "pi pi-id-card",
        route: "/profile",
      },
      {
        label: "我的课程",
        icon: "pi pi-book",
        route: "/my-courses",
      },
    ],
  },
  {
    label: "账号",
    items: [
      {
        label: "退出登录",
        icon: "pi pi-sign-out",
        command: () => {
          accountState.isLoggedIn = false;
        },
      },
    ],
  },
]);
const toggle = (event: any) => {
  avatarMenu.value.toggle(event);
};
const backgroundColor = computed(() => {
  if (accountState.username) {
    return getBackgroundColor(accountState.username);
  } else {
    return "gray";
  }
});

</script>

<template>
  <header>
    <router-link to="/" class="left">
      <img src="@/assets/pic/wooc-logo.png" />
      <h2>→砖大学WOOC</h2>
    </router-link>
    <nav>
      <router-link to="/">首页</router-link>
      <router-link to="/about">关于</router-link>
      <router-link v-if="!accountState.isLoggedIn" to="/login"
        >登录｜注册</router-link
      >
      <Avatar
        id="avatar"
        @mouseenter="toggle"
        v-if="accountState.isLoggedIn"
        :label="accountState.username?.charAt(0).toUpperCase()"
        aria-haspopup="true"
        :style="{ backgroundColor }"
        aria-controls="overlay_menu"
      />
      <Menu ref="avatarMenu" :model="items" id="overlay_menu" :popup="true">
        <template #item="{ item, props }">
          <RouterLink
            v-if="item.route"
            v-slot="{ href, navigate }"
            :to="item.route"
            custom
          >
            <a :href="href" v-bind="props.action" @click="navigate">
              <span :class="item.icon" />
              <span class="ml-2">{{ item.label }}</span>
            </a>
          </RouterLink>
          <a v-else v-bind="props.action">
            <span :class="item.icon" />
            <span class="ml-2">{{ item.label }}</span>
          </a>
        </template>
      </Menu>
    </nav>
  </header>
</template>

<style lang="css" scoped>
#avatar {
  cursor: pointer;
}

.left {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: bold;
}

a.left {
  text-decoration: none;
  color: var(--color-text);
}

.left > img {
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
