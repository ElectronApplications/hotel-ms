import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { watch } from "vue";

export function useAuthentication(hook: (isAuthenticated: boolean) => void) {
  const authStore = useAuthStore();
  const { currentUser } = storeToRefs(authStore);

  watch(
    currentUser,
    () => {
      hook(currentUser.value !== undefined);
    },
    {
      immediate: true,
    },
  );
}
