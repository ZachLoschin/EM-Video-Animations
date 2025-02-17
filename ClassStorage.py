"""
Scene to show fitting of multivariate gaussian distribution using
maximum likelihood estimation. Should be early on; we will not cover
ML estimators but use them to motivate expectation maximization for
latent variable models.
"""
class FitGaussian3D(ThreeDScene):
    def construct(self):
        # Step 1: Create 3D Axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 0.25, 0.25],
            axis_config={"color": BLUE}
        )

        # Step 2: Sample 2D Gaussian Data Points
        mean = np.array([0, 0])  
        cov = np.array([[0.25, 0], [0, 0.25]])  
        samples = np.random.multivariate_normal(mean, cov, 100)

        dots = VGroup(*[
            Dot3D(axes.c2p(x, y, 0), color=RED, radius=0.05) for x, y in samples
        ])

        # Step 3: Create the 3D Gaussian Surface
        def gaussian_surface(u, v):
            pos = np.array([u, v])
            pdf = stats.multivariate_normal(mean=mean, cov=cov).pdf(pos)
            return [u, v, pdf * 3]  

        gaussian = Surface(
            lambda u, v: np.array(gaussian_surface(u, v)),
            u_range=[-1.5, 1.5], v_range=[-1.5, 1.5],
            resolution=(30, 30),
            color=YELLOW,
            fill_opacity=0.75
        )

        # 🔹 Step 4: Set Initial Camera Zoomed Out
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, gamma=0*DEGREES, zoom=0.6)

        # Animations
        self.play(Create(axes))
        self.wait()
        self.play(FadeIn(dots))
        self.wait()

        # # 🔹 Step 5: Rotate Camera as Gaussian is Drawn
        self.begin_ambient_camera_rotation(rate=60/6 * DEGREES, about="phi")
        self.begin_ambient_camera_rotation(rate=45/6 * DEGREES, about="theta")
    
        self.wait()
        self.play(Create(gaussian), run_time=3)
        self.move_camera(
                zoom=1.0,  # Zoom in
                run_time=2,  # Time for this animation
            )
        
        self.stop_ambient_camera_rotation(about='phi')
        self.stop_ambient_camera_rotation(about='theta')

        self.wait()
