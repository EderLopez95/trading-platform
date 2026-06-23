import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  loginSchema,
  type LoginFormData,
} from "../services/loginSchema";
import styles from "./LoginForm.module.scss";
import { Link } from 'react-router-dom';
import Input from "@/shared/components/ui/Input/Input";
import Button from "@/shared/components/ui/Button/Button";

type Props = {
  onSubmit: (data: LoginFormData) => Promise<void>;
};

export default function LoginForm({
  onSubmit,
}: Props) {
  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isSubmitting,
    },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className={styles.field}>
          <label>Email</label>
          <Input
            type="email"
            autoComplete="email"
            {...register("email")}
          />
          <p className={styles.error}>
            {errors.email?.message}
          </p>
        </div>
        <div className={styles.field}>
          <label>Password</label>
          <Input
            type="password"
            autoComplete="current-password"
            {...register("password")}
          />
          <p className={styles.error}>
            {errors.password?.message}
          </p>
        </div>
        <Button
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Logging in..." : "Login"}
        </Button>
      </form>
      <div className={styles.linkWrapper}>
        <p>Don't have an account? <Link to="/register">Register here</Link></p>
      </div>
    </>
  );
}
