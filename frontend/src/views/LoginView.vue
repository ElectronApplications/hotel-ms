<script setup lang="ts">
import SurfaceCard from "@/components/SurfaceCard.vue";
import BrandIcon from "@/assets/brand-icon.svg";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { onBeforeMount, ref } from "vue";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import TextField from "@/components/TextField.vue";

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

const login_phone_number = ref("");
const login_password = ref("");

const register_phone_number = ref("");
const register_password = ref("");
const register_confirm_password = ref("");

async function loginSubmit() {
  console.log(login_phone_number.value);
  console.log(login_password.value);
}

async function registerSubmit() {
  console.log(register_phone_number.value);
  console.log(register_password.value);
  console.log(register_confirm_password.value);
}

onBeforeMount(() => {
  if (currentUser.value !== undefined) {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto flex justify-center pt-2">
    <SurfaceCard class="flex flex-col items-center">
      <BrandIcon class="scale-150" />

      <div class="pt-6">
        <TabGroup>
          <TabList
            class="flex w-[300px] flex-row space-x-1 rounded-xl bg-primary-light p-1 dark:bg-primary-dark"
          >
            <Tab v-slot="{ selected }" class="basis-1/2 outline-none"
              ><button
                class="w-full rounded-lg py-2"
                :class="[
                  selected
                    ? 'bg-surface-light text-surface-content-light shadow dark:bg-surface-dark dark:text-surface-content-dark'
                    : 'text-primary-content-light hover:bg-primary-active-light dark:text-primary-content-dark dark:hover:bg-primary-active-dark',
                ]"
              >
                Login
              </button></Tab
            >

            <Tab v-slot="{ selected }" class="basis-1/2 outline-none"
              ><button
                class="w-full rounded-lg py-2"
                :class="[
                  selected
                    ? 'bg-surface-light text-surface-content-light shadow dark:bg-surface-dark dark:text-surface-content-dark'
                    : 'text-primary-content-light hover:bg-primary-active-light dark:text-primary-content-dark dark:hover:bg-primary-active-dark',
                ]"
              >
                Register
              </button></Tab
            >
          </TabList>

          <TabPanels class="pt-4">
            <TabPanel>
              <form class="space-y-4" @submit.prevent="loginSubmit">
                <div>
                  <label for="phone_number" class="block text-sm/6 font-medium"
                    >Phone number</label
                  >
                  <TextField
                    class="mt-2"
                    v-model="login_phone_number"
                    name="phone_number"
                    type="tel"
                    autocomplete="tel"
                    :required="true"
                  />
                </div>
                <div>
                  <label for="password" class="block text-sm/6 font-medium"
                    >Password</label
                  >
                  <TextField
                    class="mt-2"
                    v-model="login_password"
                    name="password"
                    type="password"
                    autocomplete="current-password"
                    :required="true"
                  />
                </div>
                <div>
                  <PrimaryButton type="submit" class="w-full">
                    Sign in
                  </PrimaryButton>
                </div>
              </form>
            </TabPanel>

            <TabPanel>
              <form class="space-y-4" @submit.prevent="registerSubmit">
                <div>
                  <label for="phone_number" class="block text-sm/6 font-medium"
                    >Phone number</label
                  >
                  <TextField
                    class="mt-2"
                    v-model="register_phone_number"
                    name="phone_number"
                    type="tel"
                    autocomplete="tel"
                    :required="true"
                  />
                </div>
                <div>
                  <label for="password" class="block text-sm/6 font-medium"
                    >Password</label
                  >
                  <TextField
                    class="mt-2"
                    v-model="register_password"
                    name="password"
                    type="password"
                    autocomplete="current-password"
                    :required="true"
                  />
                </div>
                <div>
                  <label
                    for="confirm-password"
                    class="block text-sm/6 font-medium"
                    >Confirm password</label
                  >
                  <TextField
                    class="mt-2"
                    v-model="register_confirm_password"
                    name="confirm-password"
                    type="password"
                    autocomplete="current-password"
                    :required="true"
                  />
                </div>
                <div>
                  <PrimaryButton type="submit" class="w-full">
                    Sign up
                  </PrimaryButton>
                </div>
              </form>
            </TabPanel>
          </TabPanels>
        </TabGroup>
      </div>
    </SurfaceCard>
  </main>
</template>
