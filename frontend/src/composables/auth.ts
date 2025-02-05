import { useAuthStore } from "@/stores/auth";
import type { ClientRole } from "@/types";
import { storeToRefs } from "pinia";
import { watch } from "vue";

export function useAuthentication(hook: (isAuthenticated: boolean) => void) {
  const authStore = useAuthStore();
  const { refresh } = storeToRefs(authStore);

  watch(
    refresh,
    () => {
      hook(refresh.value !== undefined);
    },
    {
      immediate: true,
    }
  );
}

export function useUserRole(hook: (role: ClientRole) => void) {
  const authStore = useAuthStore();
  const { currentUser } = storeToRefs(authStore);

  watch(
    currentUser,
    () => {
      if (currentUser.value !== undefined) {
        hook(currentUser.value.role);
      }
    },
    {
      immediate: true,
    }
  );
}
