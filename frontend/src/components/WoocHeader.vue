<script setup lang="ts">
import { accountState } from "@/global/account";
import getBackgroundColor from "@/util/usernameBgColor";
import { Avatar } from "primevue";
import Menu from "primevue/menu";
import { computed, ref } from "vue";
import UploadIcon from "@/assets/icon/云上传.svg";
const avatarMenu = ref();
const items = ref([
  {
    label: "个人信息",
    items: [
      {
        label: "个人中心",
        icon: "pi pi-id-card",
        route: "/profile",
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
      <h2 class="text-xl">→砖大学WOOC</h2>
    </router-link>
    <nav>
      <router-link to="/offer" class="router-link" v-if="accountState.isLoggedIn && accountState.role == 'teacher'">
        <img :src="UploadIcon" width="24px" />
        <span>发布新课程</span>
      </router-link>
      <router-link to="/" class="router-link">首页</router-link>
      <router-link to="/about" class="router-link">关于</router-link>
      <router-link v-if="!accountState.isLoggedIn" to="/login" class="router-link"
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
a.router-link {
  display: flex;
  align-items: center;
  gap: 4px;
}

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
  width: 100vi;
  background-color: rgba(255, 255, 255, 0.7);
  color: var(--color-text);
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
  padding: 15px 20px;
  height: 60px;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
</style>
