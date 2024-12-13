import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";
import type { Client } from "@/types";
import { onBeforeMount, ref } from "vue";
import axios from "axios";

export const useAuthStore = defineStore("auth", () => {
  type Token = string | undefined;
  type Tokens = {
    access: string;
    refresh: string;
  };

  function isTokenValid(token: Token): boolean {
    if (token === undefined) {
      return false;
    } else {
      const decoded = jwtDecode(token);
      return Date.now() < decoded.exp! * 1000;
    }
  }

  const access = useLocalStorage<Token>("accessToken", undefined);
  const refresh = useLocalStorage<Token>("refreshToken", undefined);
  const currentUser = ref<Client>();

  async function refreshTokens() {
    const simpleAxios = axios.create();
    const newTokens: Tokens = (
      await simpleAxios.post("/api/auth/refresh/", {
        refresh: refresh.value,
      })
    ).data;

    access.value = newTokens.access;
    refresh.value = newTokens.refresh;
  }

  async function updateTokens(): Promise<boolean> {
    if (!isTokenValid(refresh.value)) {
      refresh.value = undefined;
      access.value = undefined;
      currentUser.value = undefined;
      return false;
    } else if (!isTokenValid(access.value)) {
      await refreshTokens();
    }
    return true;
  }

  async function updateUserInfo() {
    if (await updateTokens()) {
      try {
        currentUser.value = (await axios.get("/api/user/self/")).data;
      } catch(_) {
        // TODO: actual error checking
        refresh.value = undefined;
        access.value = undefined;
        currentUser.value = undefined;
      }
    }
  }

  async function login(
    phoneNumber: string,
    password: string,
  ): Promise<boolean> {
    try {
      const simpleAxios = axios.create();
      const tokens = (
        await simpleAxios.post<Tokens>("/api/auth/login/", {
          phone_number: phoneNumber,
          password: password,
        })
      ).data;
      refresh.value = tokens.refresh;
      access.value = tokens.access;
      await updateUserInfo();
      return true;
    } catch (_) {
      return false;
    }
  }

  async function logout() {
    const refreshCopy = refresh.value;
    refresh.value = undefined;
    access.value = undefined;
    currentUser.value = undefined;

    const simpleAxios = axios.create();
    await simpleAxios.post("/api/auth/logout/", {
      refresh: refreshCopy,
    });
  }

  onBeforeMount(async () => {
    await updateUserInfo();
  });

  return {
    currentUser,
    access,
    refresh,
    updateTokens,
    updateUserInfo,
    login,
    logout,
  };
});
