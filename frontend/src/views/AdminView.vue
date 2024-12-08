<script setup lang="ts">
import DefaultProfileImage from "@/assets/default-profile.png";
import { useAuthentication, useUserRole } from "@/composables/auth";
import router from "@/router";
import { clientRoles, type Client, type ClientRole } from "@/types";
import axios from "axios";
import { onMounted, ref } from "vue";
import ExpandableImage from "@/components/ExpandableImage.vue";
import EditableLabel from "@/components/EditableLabel.vue";
import SelectList from "@/components/SelectList.vue";

const clients = ref<Client[]>([]);

async function fetchClients() {
  clients.value = (await axios.get("/api/client/")).data;
}

async function changeClientName(client: Client, newName: string) {
  if (client.name !== newName) {
    await axios.put(`/api/client/${client.id}/`, {
      name: newName,
    });
    await fetchClients();
  }
}

async function changeClientPhoneNumber(client: Client, newPhoneNumber: string) {
  if (client.phone_number !== newPhoneNumber) {
    await axios.put(`/api/client/${client.id}/`, {
      phone_number: newPhoneNumber,
    });
    await fetchClients();
  }
}

async function changeClientRole(client: Client, newRole: ClientRole) {
  if (client.role !== newRole) {
    await axios.put(`/api/client/${client.id}/`, {
      role: newRole,
    });
    await fetchClients();
  }
}

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});

useUserRole((role) => {
  if (role !== "admin") {
    router.push("/profile");
  }
});

onMounted(async () => {
  await fetchClients();
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <h1 class="text-center text-4xl font-extrabold lg:text-start">
      Hotel clients
    </h1>
    <div
      class="mt-4 rounded-3xl bg-slate-100 px-0 py-6 text-surface-content-light shadow-md dark:bg-secondary-dark dark:text-surface-content-dark"
    >
      <table
        class="w-full table-auto bg-slate-100 text-center dark:bg-secondary-dark"
      >
        <thead
          class="border-b border-secondary-light dark:border-secondary-active-dark"
        >
          <tr>
            <th class="py-2">Name</th>
            <th class="py-2">Phone number</th>
            <th class="py-2">Role</th>
            <th class="py-2">Profile image</th>
          </tr>
        </thead>
        <tbody class="bg-surface-light dark:bg-surface-dark">
          <tr v-for="client in clients" v-bind:key="client.id">
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              <EditableLabel
                v-if="client.role !== 'admin'"
                class="justify-center"
                :text="client.name"
                @updateText="(value) => changeClientName(client, value)"
              />
              <span v-if="client.role === 'admin'">
                {{ client.name }}
              </span>
            </td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              <EditableLabel
                v-if="client.role !== 'admin'"
                class="justify-center"
                :text="client.phone_number"
                @updateText="(value) => changeClientPhoneNumber(client, value)"
              />
              <span v-if="client.role === 'admin'">
                {{ client.phone_number }}
              </span>
            </td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              <SelectList
                v-if="client.role !== 'admin'"
                :options="clientRoles"
                :selected="clientRoles.indexOf(client.role)"
                @updateSelection="
                  (value) => changeClientRole(client, clientRoles[value])
                "
              />
              <span v-if="client.role === 'admin'">
                {{ client.role }}
              </span>
            </td>
            <td
              class="border-b border-secondary-light py-2 dark:border-secondary-active-dark"
            >
              <ExpandableImage
                imgClass="w-[64px]"
                :src="client.picture ?? DefaultProfileImage"
                :alt="client.name"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="mt-4">
      <a href="/admin" class="font-bold text-blue-500 underline"
        >Django admin page</a
      >
    </div>
  </main>
</template>
